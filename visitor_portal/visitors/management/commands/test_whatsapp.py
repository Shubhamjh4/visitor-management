from django.core.management.base import BaseCommand
from visitors.sms import send_whatsapp, send_message


class Command(BaseCommand):
    help = 'Test WhatsApp messaging functionality'

    def add_arguments(self, parser):
        parser.add_argument(
            '--phone',
            type=str,
            help='Phone number to send test message to (e.g., +919876543210)',
            required=True
        )
        parser.add_argument(
            '--message',
            type=str,
            default='Hello! This is a test WhatsApp message from your Visitor Management System.',
            help='Message to send (default: test message)'
        )
        parser.add_argument(
            '--type',
            type=str,
            choices=['whatsapp', 'sms'],
            default='whatsapp',
            help='Message type: whatsapp or sms (default: whatsapp)'
        )

    def handle(self, *args, **options):
        phone = options['phone']
        message = options['message']
        msg_type = options['type']
        
        self.stdout.write(
            self.style.SUCCESS(f'Sending {msg_type.upper()} message to {phone}...')
        )
        
        try:
            if msg_type == 'whatsapp':
                result = send_whatsapp(phone, message)
            else:
                from visitors.sms import send_sms
                result = send_sms(phone, message)
            
            if result:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ {msg_type.upper()} sent successfully! Message ID: {result}')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f'❌ Failed to send {msg_type.upper()}. Check your configuration.')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error sending {msg_type.upper()}: {str(e)}')
            )
