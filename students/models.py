"""Database models for the students app."""
from django.core.validators import RegexValidator
from django.db import models


class Student(models.Model):
    """One row in the students table."""

    YEAR_CHOICES = [
        ("1st Year", "1st Year"),
        ("2nd Year", "2nd Year"),
        ("3rd Year", "3rd Year"),
        ("4th Year", "4th Year"),
    ]
    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]

    # Only digits, optionally starting with +, 7 to 15 characters long
    phone_validator = RegexValidator(
        regex=r"^\+?\d{7,15}$",
        message="Enter a valid phone number (7-15 digits, may start with +).",
    )

    full_name = models.CharField(max_length=100)
    roll_number = models.CharField(
        max_length=30,
        unique=True,
        error_messages={"unique": "A student with this roll number already exists."},
    )
    email = models.EmailField()
    phone_number = models.CharField(max_length=16, validators=[phone_validator])
    course = models.CharField(max_length=100)
    year = models.CharField(max_length=10, choices=YEAR_CHOICES)
    address = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.full_name} ({self.roll_number})"
