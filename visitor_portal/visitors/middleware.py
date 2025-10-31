from django.shortcuts import redirect
from django.urls import reverse


class AdminAccessMiddleware:
    """
    Middleware to restrict admin access to superusers only.
    Guards and regular staff are redirected to dashboard.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is trying to access admin
        if request.path.startswith('/admin/'):
            # Allow access to admin login page
            if request.path == '/admin/login/' or request.path == '/admin/logout/':
                response = self.get_response(request)
                return response
            
            # Check if user is authenticated
            if request.user.is_authenticated:
                # Only superusers can access admin
                if not request.user.is_superuser:
                    # Redirect guards and staff to dashboard
                    return redirect('dashboard')
            else:
                # Allow unauthenticated users to access admin login
                response = self.get_response(request)
                return response
        
        response = self.get_response(request)
        return response
