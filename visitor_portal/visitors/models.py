from django.db import models
from django.utils import timezone


class Employee(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    department = models.CharField(max_length=120, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.department})" if self.department else self.name


class Visitor(models.Model):
    GOVT_ID_TYPES = [
        ("aadhaar", "Aadhaar"),
        ("pan", "PAN"),
        ("passport", "Passport"),
        ("other", "Other"),
    ]

    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField()
    photo = models.ImageField(upload_to="visitor_photos/", blank=True, null=True)
    govt_id_type = models.CharField(max_length=20, choices=GOVT_ID_TYPES, blank=True)
    govt_id_image = models.ImageField(upload_to="visitor_ids/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.full_name


class Visit(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("ongoing", "Ongoing"),
        ("ended", "Ended"),
    ]

    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name="visits")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="visits")
    purpose = models.CharField(max_length=255, blank=True)
    started_at = models.DateTimeField(default=timezone.now)
    ended_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ongoing")
    sms_sent_at = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True)

    @property
    def duration_seconds(self) -> int:
        if self.ended_at:
            return int((self.ended_at - self.started_at).total_seconds())
        return int((timezone.now() - self.started_at).total_seconds())

    def __str__(self) -> str:
        return f"Visit: {self.visitor} -> {self.employee} ({self.status})"

# Create your models here.
