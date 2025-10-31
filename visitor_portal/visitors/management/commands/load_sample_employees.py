from django.core.management.base import BaseCommand

from visitors.models import Employee


class Command(BaseCommand):
    help = "Load a sample employee into the database"

    def handle(self, *args, **options):
        emp, created = Employee.objects.get_or_create(
            name="Om Prakash Jha",
            defaults={
                "department": "HR",
                "phone": "+919810764712",
                "email": "",
                "active": True,
            },
        )
        if not created:
            emp.department = "HR"
            emp.phone = "+919810764712"
            emp.active = True
            emp.save()
        self.stdout.write(self.style.SUCCESS(f"Employee ready: {emp.name} ({emp.department})"))


