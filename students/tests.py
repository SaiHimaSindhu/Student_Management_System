"""Automated tests:  python manage.py test"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Student

User = get_user_model()

STUDENT = dict(
    full_name="Test Student", roll_number="R001", email="t@example.com",
    phone_number="9876543210", course="CS", year="1st Year",
    address="Somewhere", status="active",
)


class AuthTests(TestCase):
    def test_signup_login_logout(self):
        r = self.client.post(reverse("signup"), dict(
            full_name="Jane Doe", email="jane@example.com", username="jane",
            password1="Str0ng!Pass99", password2="Str0ng!Pass99"))
        self.assertRedirects(r, reverse("login"))
        self.assertEqual(User.objects.get(username="jane").get_full_name(), "Jane Doe")
        # login by email
        r = self.client.post(reverse("login"), dict(identifier="jane@example.com", password="Str0ng!Pass99"))
        self.assertRedirects(r, reverse("dashboard"))
        # logout
        r = self.client.post(reverse("logout"))
        self.assertRedirects(r, reverse("login"))
        self.assertEqual(self.client.get(reverse("dashboard")).status_code, 302)

    def test_signup_validation(self):
        r = self.client.post(reverse("signup"), dict(
            full_name="A", email="bad", username="a", password1="x", password2="y"))
        self.assertEqual(r.status_code, 200)
        self.assertFalse(User.objects.exists())

    def test_bad_login(self):
        r = self.client.post(reverse("login"), dict(identifier="nobody", password="nope"))
        self.assertContains(r, "Invalid username/email or password.")


class StudentTests(TestCase):
    def setUp(self):
        User.objects.create_user("demo", "demo@example.com", "Demo@12345")
        self.client.login(username="demo", password="Demo@12345")

    def test_pages_load(self):
        for name in ("dashboard", "add_student", "view_students", "profile"):
            self.assertEqual(self.client.get(reverse(name)).status_code, 200, name)

    def test_crud(self):
        r = self.client.post(reverse("add_student"), STUDENT)
        self.assertRedirects(r, reverse("view_students"))
        s = Student.objects.get()
        # duplicate roll number rejected
        r = self.client.post(reverse("add_student"), STUDENT)
        self.assertContains(r, "already exists")
        self.assertEqual(Student.objects.count(), 1)
        # edit
        self.assertContains(self.client.get(reverse("edit_student", args=[s.pk])), "Test Student")
        self.client.post(reverse("edit_student", args=[s.pk]), {**STUDENT, "full_name": "Renamed"})
        s.refresh_from_db()
        self.assertEqual(s.full_name, "Renamed")
        # delete (GET shows confirmation, POST deletes)
        self.assertContains(self.client.get(reverse("delete_student", args=[s.pk])), "Are you sure")
        self.assertEqual(Student.objects.count(), 1)
        self.client.post(reverse("delete_student", args=[s.pk]))
        self.assertEqual(Student.objects.count(), 0)

    def test_search_and_pagination(self):
        for i in range(12):
            Student.objects.create(**{**STUDENT, "roll_number": f"R{i:03d}", "full_name": f"Name{i}"})
        r = self.client.get(reverse("view_students"))
        self.assertEqual(len(r.context["page"]), 5)
        self.assertEqual(r.context["page"].paginator.num_pages, 3)
        r = self.client.get(reverse("view_students"), {"q": "R011"})
        self.assertEqual(len(r.context["page"]), 1)
        r = self.client.get(reverse("view_students"), {"q": "t@example.com"})
        self.assertEqual(r.context["page"].paginator.count, 12)

    def test_dashboard_counts(self):
        Student.objects.create(**STUDENT)
        Student.objects.create(**{**STUDENT, "roll_number": "R2", "status": "inactive"})
        r = self.client.get(reverse("dashboard"))
        self.assertEqual((r.context["total"], r.context["active"], r.context["inactive"], r.context["new"]), (2, 1, 1, 2))

    def test_profile_update_and_password(self):
        r = self.client.post(reverse("profile"), dict(
            action="profile", full_name="New Name", username="demo", email="new@example.com"))
        self.assertRedirects(r, reverse("profile"))
        self.assertEqual(User.objects.get().email, "new@example.com")
        r = self.client.post(reverse("profile"), dict(
            action="password", old_password="Demo@12345",
            new_password1="An0ther!Pass77", new_password2="An0ther!Pass77"))
        self.assertRedirects(r, reverse("profile"))
        self.assertTrue(User.objects.get().check_password("An0ther!Pass77"))
        self.assertEqual(self.client.get(reverse("dashboard")).status_code, 200)  # still logged in
