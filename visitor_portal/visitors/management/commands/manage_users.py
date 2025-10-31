from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Manage users for the visitor management system'

    def add_arguments(self, parser):
        parser.add_argument(
            'action',
            choices=['create', 'reset', 'deactivate', 'activate', 'list'],
            help='Action to perform: create, reset, deactivate, activate, or list users'
        )
        parser.add_argument(
            '--username',
            type=str,
            help='Username for the action'
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Email address for the user'
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Password for the user (for create action)'
        )
        parser.add_argument(
            '--make-admin',
            action='store_true',
            help='Make user a superuser (for create action)'
        )

    def handle(self, *args, **options):
        action = options['action']
        
        if action == 'create':
            self.create_user(options)
        elif action == 'reset':
            self.reset_password(options)
        elif action == 'deactivate':
            self.deactivate_user(options)
        elif action == 'activate':
            self.activate_user(options)
        elif action == 'list':
            self.list_users(options)

    def create_user(self, options):
        username = options.get('username')
        email = options.get('email')
        password = options.get('password')
        make_admin = options.get('make_admin', False)

        if not username or not email or not password:
            raise CommandError('Username, email, and password are required for user creation')

        if User.objects.filter(username=username).exists():
            raise CommandError(f'User "{username}" already exists')

        if User.objects.filter(email=email).exists():
            raise CommandError(f'Email "{email}" is already in use')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=make_admin,
            is_superuser=make_admin
        )

        # Add to Guard group if not admin
        if not make_admin:
            guard_group, created = Group.objects.get_or_create(name='Guard')
            user.groups.add(guard_group)
        else:
            # For superusers, ensure they have staff status but not in Guard group
            user.is_staff = True
            user.is_superuser = True
            user.save()

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created user "{username}"')
        )

        # Send welcome email
        try:
            send_mail(
                'Welcome to Visitor Management System',
                f'''Hello {username},

Your account has been created successfully.

Login Details:
- Username: {username}
- Email: {email}

You can now access the visitor management system.

Best regards,
Visitor Management Team''',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=True,
            )
            self.stdout.write(
                self.style.SUCCESS(f'Welcome email sent to {email}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'Could not send welcome email: {e}')
            )

    def reset_password(self, options):
        username = options.get('username')
        
        if not username:
            raise CommandError('Username is required for password reset')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f'User "{username}" does not exist')

        # Generate a random password
        import secrets
        import string
        new_password = ''.join(secrets.choices(string.ascii_letters + string.digits, k=12))
        
        user.set_password(new_password)
        user.save()

        self.stdout.write(
            self.style.SUCCESS(f'Password reset for user "{username}"')
        )
        self.stdout.write(
            self.style.WARNING(f'New password: {new_password}')
        )
        self.stdout.write(
            self.style.WARNING('IMPORTANT: Save this password securely and share it with the user')
        )

        # Send password reset email
        try:
            send_mail(
                'Password Reset - Visitor Management System',
                f'''Hello {username},

Your password has been reset by an administrator.

New Login Details:
- Username: {username}
- New Password: {new_password}

Please log in and change your password immediately for security.

Best regards,
Visitor Management Team''',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=True,
            )
            self.stdout.write(
                self.style.SUCCESS(f'Password reset email sent to {user.email}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'Could not send password reset email: {e}')
            )

    def deactivate_user(self, options):
        username = options.get('username')
        
        if not username:
            raise CommandError('Username is required for deactivation')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f'User "{username}" does not exist')

        user.is_active = False
        user.save()

        self.stdout.write(
            self.style.SUCCESS(f'User "{username}" has been deactivated')
        )

        # Send deactivation email
        try:
            send_mail(
                'Account Deactivated - Visitor Management System',
                f'''Hello {username},

Your account has been deactivated by an administrator.

If you believe this is an error, please contact your system administrator.

Best regards,
Visitor Management Team''',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=True,
            )
            self.stdout.write(
                self.style.SUCCESS(f'Deactivation email sent to {user.email}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'Could not send deactivation email: {e}')
            )

    def activate_user(self, options):
        username = options.get('username')
        
        if not username:
            raise CommandError('Username is required for activation')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f'User "{username}" does not exist')

        user.is_active = True
        user.save()

        self.stdout.write(
            self.style.SUCCESS(f'User "{username}" has been activated')
        )

    def list_users(self, options):
        users = User.objects.all().order_by('username')
        
        if not users.exists():
            self.stdout.write(self.style.WARNING('No users found'))
            return

        self.stdout.write(self.style.SUCCESS('Users in the system:'))
        self.stdout.write('-' * 80)
        
        for user in users:
            status = 'Active' if user.is_active else 'Inactive'
            admin_status = 'Admin' if user.is_superuser else 'User'
            groups = ', '.join([group.name for group in user.groups.all()])
            
            self.stdout.write(
                f'Username: {user.username:<15} | '
                f'Email: {user.email:<25} | '
                f'Status: {status:<8} | '
                f'Type: {admin_status:<5} | '
                f'Groups: {groups}'
            )
