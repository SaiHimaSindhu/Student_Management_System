"""Create a demo login and sample students:  python manage.py seed_demo"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from students.models import Student

SAMPLES = [
    ("Aarav Sharma", "CS2024001", "Computer Science", "1st Year"),
    ("Priya Nair", "CS2024002", "Computer Science", "2nd Year"),
    ("Rohan Mehta", "EC2023010", "Electronics", "3rd Year"),
    ("Sneha Reddy", "ME2022005", "Mechanical", "4th Year"),
    ("Karthik Iyer", "CS2023011", "Computer Science", "3rd Year"),
    ("Ananya Das", "BT2024003", "Biotechnology", "1st Year"),
    ("Vikram Singh", "CE2022008", "Civil", "4th Year"),
    ("Meera Pillai", "EC2024004", "Electronics", "2nd Year"),
]


class Command(BaseCommand):
    help = "Creates a demo user (demo / Demo@12345) and sample students."

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username="demo").exists():
            User.objects.create_user(
                "demo", "demo@example.com", "Demo@12345", first_name="Demo", last_name="User"
            )
        for i, (name, roll, course, year) in enumerate(SAMPLES):
            Student.objects.get_or_create(
                roll_number=roll,
                defaults=dict(
                    full_name=name,
                    email=f"{name.split()[0].lower()}@college.edu",
                    phone_number=f"98765432{i:02d}",
                    course=course,
                    year=year,
                    address=f"{10 + i}, College Road, Hyderabad",
                    status="inactive" if i in (3, 6) else "active",
                ),
            )
        self.stdout.write(self.style.SUCCESS("Demo data ready. Login: demo / Demo@12345"))
