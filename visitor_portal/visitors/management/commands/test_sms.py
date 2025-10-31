from django.core.management.base import BaseCommand, CommandError

from visitors.sms import send_sms


class Command(BaseCommand):
    help = "Send a test SMS via Twilio using env credentials. Usage: python manage.py test_sms +15551234567 'Hello'"

    def add_arguments(self, parser):
        parser.add_argument("to_phone", type=str, help="Recipient phone in E.164, e.g. +15551234567")
        parser.add_argument("message", nargs="?", default="Test message from Visitor Portal", help="Message body")

    def handle(self, *args, **options):
        to_phone = options["to_phone"].strip()
        message = options["message"]

        sid = send_sms(to_phone, message)
        if sid:
            self.stdout.write(self.style.SUCCESS(f"Sent. SID: {sid}"))
        else:
            raise CommandError("SMS not sent. Check env vars TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER and package installation.")


