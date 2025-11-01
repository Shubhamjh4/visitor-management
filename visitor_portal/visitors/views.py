from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.contrib.auth.decorators import login_required, user_passes_test
from django import forms
from django.http import JsonResponse

from .models import Employee, Visitor, Visit
from .email import send_otp_email, send_visitor_notification_email


class VisitorForm(forms.ModelForm):
    employee_name = forms.CharField(max_length=200, required=True, label="Whom to meet")
    purpose = forms.CharField(max_length=255, required=True, label="Purpose of meeting")
    otp = forms.CharField(max_length=6, required=False, label="OTP (sent to email)")

    class Meta:
        model = Visitor
        fields = [
            "full_name",
            "email",
            "address",
            "phone",
        ]
        labels = {
            "full_name": "Name",
            "email": "Email",
            "address": "Address",
            "phone": "Phone",
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'required': True}),
            'email': forms.EmailInput(attrs={'required': True}),
            'address': forms.Textarea(attrs={'required': True}),
            'phone': forms.TextInput(attrs={'required': True}),
        }


class IntakeView(View):
    def get(self, request):
        form = VisitorForm()
        active_visit = None
        visit_id = request.session.get("active_visit_id")
        if visit_id:
            try:
                candidate = Visit.objects.get(id=visit_id)
                if candidate.ended_at is None:
                    active_visit = candidate
            except Visit.DoesNotExist:
                request.session.pop("active_visit_id", None)
        employees = list(Employee.objects.filter(active=True).values("id", "name", "department"))
        return render(request, "visitors/intake.html", {"form": form, "active_visit": active_visit, "employees": employees})

    def post(self, request):
        # If there is an ongoing visit in this session, redirect to it
        visit_id = request.session.get("active_visit_id")
        if visit_id:
            try:
                existing = Visit.objects.get(id=visit_id)
                if existing.ended_at is None:
                    return redirect(reverse("visit_detail", args=[existing.id]))
            except Visit.DoesNotExist:
                request.session.pop("active_visit_id", None)

        form = VisitorForm(request.POST)

        # If the user clicked Send OTP, we only need a syntactically valid email
        if request.POST.get("action") == "send_otp":
            email_input = (request.POST.get("email") or "").strip()
            employees = list(Employee.objects.filter(active=True).values("id", "name", "department"))
            if not email_input:
                if request.headers.get("x-requested-with") == "XMLHttpRequest":
                    return JsonResponse({"ok": False, "error": "Enter an email address first"}, status=400)
                form.add_error("email", "Enter an email address first")
                return render(request, "visitors/intake.html", {"form": form, "employees": employees})

            # Generate and send OTP without validating full form yet
            now_ts = int(timezone.now().timestamp())
            import random
            code = str(random.randint(100000, 999999))
            expires_ts = now_ts + 300
            request.session["otp_data"] = {"email": email_input, "code": code, "expires_ts": expires_ts}
            request.session.modified = True
            result = send_otp_email(email_input, code)
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                if result:
                    return JsonResponse({"ok": True, "otp_sent": True})
                return JsonResponse({"ok": False, "error": "Could not send OTP. Check email address and try again."}, status=400)
            context = {"form": form, "employees": employees}
            if result:
                context["otp_sent"] = True
            else:
                form.add_error("email", "Could not send OTP. Check email address and try again.")
            return render(request, "visitors/intake.html", context)

        if not form.is_valid():
            employees = list(Employee.objects.filter(active=True).values("id", "name", "department"))
            return render(request, "visitors/intake.html", {"form": form, "employees": employees})

        email = form.cleaned_data["email"].strip()
        provided_otp = (form.cleaned_data.get("otp") or "").strip()

        # Session-based OTP store
        otp_data = request.session.get("otp_data") or {}
        now_ts = int(timezone.now().timestamp())

        def _generate_code() -> str:
            import random
            return str(random.randint(100000, 999999))

        # Validate OTP; if missing or mismatched, send or resend
        otp_valid = False
        if otp_data and otp_data.get("email") == email and otp_data.get("code") == provided_otp:
            # Check expiry (5 minutes)
            if now_ts <= int(otp_data.get("expires_ts", 0)):
                otp_valid = True

        if not otp_valid:
            # Create new code if none exists for this email or expired/mismatch
            code = _generate_code()
            expires_ts = now_ts + 300  # 5 minutes
            request.session["otp_data"] = {"email": email, "code": code, "expires_ts": expires_ts}
            request.session.modified = True

            # Send OTP via Email
            result = send_otp_email(email, code)

            # Ask user to input the code
            if not result:
                form.add_error("email", "Could not send OTP. Check email address and try again.")
                employees = list(Employee.objects.filter(active=True).values("id", "name", "department"))
                return render(request, "visitors/intake.html", {"form": form, "employees": employees})
            form.add_error("otp", "Enter the OTP sent to your email")
            employees = list(Employee.objects.filter(active=True).values("id", "name", "department"))
            return render(request, "visitors/intake.html", {"form": form, "otp_sent": True, "employees": employees})

        # OTP valid; proceed to create records
        # Resolve employee from the single free-text field with suggestions
        emp_name = (form.cleaned_data.get("employee_name") or request.POST.get("employee_name") or "").strip()
        employee = None
        if emp_name:
            employee = Employee.objects.filter(active=True, name__iexact=emp_name).first() or \
                       Employee.objects.filter(active=True, name__icontains=emp_name).first()
        if employee is None:
            form.add_error("employee_name", "Please choose a valid employee")
            employees = list(Employee.objects.filter(active=True).values("id", "name", "department"))
            return render(request, "visitors/intake.html", {"form": form, "employees": employees})

        visitor = form.save()

        visit = Visit.objects.create(
            visitor=visitor,
            employee=employee,
            purpose=form.cleaned_data.get("purpose", ""),
            status="ongoing",
            started_at=timezone.now(),
        )

        # Clear OTP data
        try:
            request.session.pop("otp_data", None)
        except Exception:
            pass

        # Track the active visit in the user's session
        request.session["active_visit_id"] = visit.id

        # Notify employee with visitor name and phone via email
        purpose_text = form.cleaned_data.get("purpose", "visit") or "visit"
        result = send_visitor_notification_email(
            to_email=employee.email,
            visitor_name=visitor.full_name,
            visitor_phone=visitor.phone,
            purpose=purpose_text
        )
        if result is not None:
            visit.sms_sent_at = timezone.now()
        visit.save(update_fields=["sms_sent_at"])

        return redirect(reverse("visit_detail", args=[visit.id]))


def visit_detail(request, visit_id: int):
    visit = get_object_or_404(Visit, id=visit_id)
    if visit.ended_at is None:
        request.session["active_visit_id"] = visit.id
    return render(request, "visitors/visit_detail.html", {"visit": visit})


def end_visit(request, visit_id: int):
    visit = get_object_or_404(Visit, id=visit_id)
    if visit.ended_at is None:
        visit.ended_at = timezone.now()
        visit.status = "ended"
        visit.save(update_fields=["ended_at", "status"])
    # Clear active visit from session if it matches
    if request.session.get("active_visit_id") == visit.id:
        request.session.pop("active_visit_id", None)
    return redirect(reverse("visit_detail", args=[visit.id]))


def _is_guard(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name='Guard').exists())


@user_passes_test(_is_guard, login_url='/login/')
def dashboard(request):
    from django.db.models import Q
    from datetime import datetime, timedelta
    import calendar
    
    # Get search query and month filter from request
    search_query = request.GET.get('search', '').strip()
    month_filter = request.GET.get('month', '').strip()
    
    # Base querysets
    ongoing_base = Visit.objects.filter(status="ongoing")
    recent_base = Visit.objects.filter(status="ended")
    
    # Apply month filter if specified
    if month_filter:
        try:
            # Parse month filter (format: YYYY-MM)
            year, month = map(int, month_filter.split('-'))
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1)
            else:
                end_date = datetime(year, month + 1, 1)
            
            ongoing_base = ongoing_base.filter(started_at__gte=start_date, started_at__lt=end_date)
            recent_base = recent_base.filter(started_at__gte=start_date, started_at__lt=end_date)
        except (ValueError, IndexError):
            # Invalid month format, ignore filter
            pass
    
    # Apply search filter if specified
    if search_query:
        search_filter = Q(
            visitor__full_name__icontains=search_query
        ) | Q(
            visitor__phone__icontains=search_query
        ) | Q(
            employee__name__icontains=search_query
        ) | Q(
            employee__department__icontains=search_query
        ) | Q(
            purpose__icontains=search_query
        )
        
        ongoing_base = ongoing_base.filter(search_filter)
        recent_base = recent_base.filter(search_filter)
    
    # Final querysets - optimize with select_related for faster queries
    # Smart limiting based on filters
    has_filters = bool(search_query or month_filter)
    
    # Ongoing visits: Always show all (critical for monitoring active visits)
    # But cap at 100 to prevent performance issues
    ongoing = ongoing_base.select_related('visitor', 'employee').order_by("-started_at")[:100]
    
    # Recent visits: Limit on initial load, show more when filtering
    if has_filters:
        # When filtering/searching: show up to 100 results
        recent = recent_base.select_related('visitor', 'employee').order_by("-ended_at")[:100]
    else:
        # Initial load: limit to 20 for mobile performance
        recent = recent_base.select_related('visitor', 'employee').order_by("-ended_at")[:20]
    
    # Get available months for filter dropdown
    available_months = []
    current_year = datetime.now().year
    for year in range(current_year - 1, current_year + 1):
        for month in range(1, 13):
            month_name = calendar.month_name[month]
            month_value = f"{year}-{month:02d}"
            available_months.append({
                'value': month_value,
                'label': f"{month_name} {year}"
            })
    
    # If this is an AJAX request, return JSON
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        from django.template.loader import render_to_string
        
        ongoing_html = render_to_string('visitors/partials/ongoing_visits.html', {
            'ongoing': ongoing
        })
        recent_html = render_to_string('visitors/partials/recent_visits.html', {
            'recent': recent
        })
        
        return JsonResponse({
            'ongoing_html': ongoing_html,
            'recent_html': recent_html,
            'ongoing_count': ongoing.count(),
            'recent_count': recent.count()
        })
    
    return render(
        request,
        "visitors/dashboard.html",
        {
            "ongoing": ongoing, 
            "recent": recent,
            "search_query": search_query,
            "month_filter": month_filter,
            "available_months": available_months
        },
    )


@user_passes_test(_is_guard, login_url='/login/')
def guard_visit_detail(request, visit_id: int):
    visit = get_object_or_404(Visit, id=visit_id)
    return render(request, "visitors/visit_admin_detail.html", {"visit": visit})

# Create your views here.
