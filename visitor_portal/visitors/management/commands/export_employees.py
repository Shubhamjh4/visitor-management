from django.core.management.base import BaseCommand
from visitors.models import Employee
import csv
import sys


class Command(BaseCommand):
    help = "Export employees to CSV with headers: name,department,phone,email,active"

    def add_arguments(self, parser):
        parser.add_argument('--out', type=str, default='-', help='Output file path or - for stdout')

    def handle(self, *args, **options):
        out = options['out']
        fieldnames = ['name', 'department', 'phone', 'email', 'active']
        if out == '-' or out == '':
            writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
            writer.writeheader()
            for e in Employee.objects.all().order_by('name'):
                writer.writerow({
                    'name': e.name,
                    'department': e.department,
                    'phone': e.phone,
                    'email': e.email,
                    'active': '1' if e.active else '0',
                })
        else:
            with open(out, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for e in Employee.objects.all().order_by('name'):
                    writer.writerow({
                        'name': e.name,
                        'department': e.department,
                        'phone': e.phone,
                        'email': e.email,
                        'active': '1' if e.active else '0',
                    })
            self.stdout.write(self.style.SUCCESS(f"Exported employees to {out}"))


