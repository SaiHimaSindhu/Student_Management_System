from django.core.validators import RegexValidator
from django.db import models


class Student(models.Model):
    """
    Represents a single student record managed by the Student
    Management System.
    """

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    COURSE_CHOICES = (
        ('BCA', 'BCA'),
        ('BSc Computer Science', 'BSc Computer Science'),
        ('BTech CSE', 'BTech CSE'),
        ('MCA', 'MCA'),
        ('MSc Computer Science', 'MSc Computer Science'),
        ('MBA', 'MBA'),
        ('Other', 'Other'),
    )

    # Validator to make sure roll numbers only contain letters,
    # numbers and hyphens (no spaces / special characters).
    roll_number_validator = RegexValidator(
        regex=r'^[A-Za-z0-9\-]+$',
        message='Roll number can only contain letters, numbers and hyphens.'
    )

    # Validator for a simple phone number (7-15 digits, optional +).
    phone_validator = RegexValidator(
        regex=r'^\+?\d{7,15}$',
        message='Enter a valid phone number (7-15 digits, optional leading +).'
    )

    student_name = models.CharField(
        max_length=100,
        help_text='Full name of the student.'
    )

    # unique=True enforces the "unique roll number" requirement at the
    # database level. The form validation layer also surfaces a
    # friendly error message before hitting the DB.
    roll_number = models.CharField(
        max_length=20,
        unique=True,
        validators=[roll_number_validator],
        help_text='Unique roll number for the student.'
    )

    # EmailField performs built-in email format validation.
    email = models.EmailField(
        max_length=150,
        help_text='A valid email address.'
    )

    phone = models.CharField(
        max_length=15,
        validators=[phone_validator],
        help_text='Contact phone number.'
    )

    course = models.CharField(
        max_length=50,
        choices=COURSE_CHOICES,
        default='BCA',
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default='Other',
    )

    address = models.TextField(
        help_text='Residential address of the student.'
    )

    # Profile photo is optional so the form still works even if the
    # student doesn't have a photo to upload.
    profile_photo = models.ImageField(
        upload_to='student_photos/',
        blank=True,
        null=True,
        help_text='Upload a profile photo (optional).'
    )

    joining_date = models.DateField(
        help_text='Date the student joined the institute.'
    )

    # Automatically managed timestamp, useful for ordering / auditing.
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.student_name} ({self.roll_number})'
