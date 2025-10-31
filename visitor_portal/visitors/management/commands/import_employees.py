from django.core.management.base import BaseCommand, CommandError
from visitors.models import Employee
import csv
from typing import Optional


def normalize_phone(raw: str) -> str:
    s = (raw or "").strip()
    # If 10 digits (likely India), keep as-is; our sms layer will prefix +91
    digits = ''.join(ch for ch in s if ch.isdigit())
    return digits


class Command(BaseCommand):
    help = "Import or update employees from a CSV file with headers: name,department,phone[,email][,active]"

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='Path to employees CSV')
        parser.add_argument('--deactivate-missing', action='store_true', help='Mark employees not present in CSV as inactive')

    def handle(self, *args, **options):
        path = options['csv_path']
        deactivate_missing = options['deactivate_missing']
        try:
            with open(path, newline='', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                required = {'name', 'department', 'phone'}
                if not required.issubset({h.strip().lower() for h in reader.fieldnames or []}):
                    raise CommandError('CSV must include headers: name, department, phone')

                seen_names = set()
                created = 0
                updated = 0
                for row in reader:
                    name = (row.get('name') or '').strip()
                    dept = (row.get('department') or '').strip()
                    phone = normalize_phone(row.get('phone') or '')
                    email = (row.get('email') or '').strip()
                    active_raw = (row.get('active') or '').strip().lower()
                    active = True if active_raw in ('', '1', 'true', 'yes', 'y') else False

                    if not name or not phone:
                        continue

                    emp, is_created = Employee.objects.get_or_create(name=name, defaults={
                        'department': dept,
                        'phone': phone,
                        'email': email,
                        'active': active,
                    })
                    if is_created:
                        created += 1
                    else:
                        changed = False
                        if emp.department != dept:
                            emp.department = dept; changed = True
                        if emp.phone != phone:
                            emp.phone = phone; changed = True
                        if email and emp.email != email:
                            emp.email = email; changed = True
                        if emp.active != active:
                            emp.active = active; changed = True
                        if changed:
                            emp.save()
                            updated += 1
                    seen_names.add(name)

                if deactivate_missing:
                    qs = Employee.objects.filter(active=True).exclude(name__in=seen_names)
                    count = qs.update(active=False)
                    self.stdout.write(self.style.WARNING(f"Deactivated {count} employees not in CSV"))

                self.stdout.write(self.style.SUCCESS(f"Employees import complete. Created: {created}, Updated: {updated}"))
        except FileNotFoundError:
            raise CommandError(f'File not found: {path}')
        except Exception as e:
            raise CommandError(str(e))


