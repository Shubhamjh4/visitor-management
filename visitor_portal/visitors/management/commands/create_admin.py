"""
Temporary command to create admin user via Render deployment.
Usage: python manage.py create_admin
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    help = 'Create or update admin superuser'

    def handle(self, *args, **options):
        # Get credentials from environment variables
        admin_username = os.getenv('ADMIN_USERNAME', 'admin')
        admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
        admin_password = os.getenv('ADMIN_PASSWORD', 'changeme123')
        
        # Check if user exists
        if User.objects.filter(username=admin_username).exists():
            user = User.objects.get(username=admin_username)
            user.set_password(admin_password)
            user.email = admin_email
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully updated admin user "{admin_username}"')
            )
        else:
            # Create new superuser
            User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created admin user "{admin_username}"')
            )
        
        self.stdout.write(
            self.style.WARNING(f'Username: {admin_username}')
        )
        self.stdout.write(
            self.style.WARNING(f'Password: {admin_password}')
        )
        self.stdout.write(
            self.style.WARNING('⚠️ IMPORTANT: Delete this file and remove environment variables after first use!')
        )

