"""Views: the "V" in Django's MVT (Model-View-Template) pattern."""
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import (
    LoginForm, ProfileForm, SignupForm, StudentForm, StyledPasswordChangeForm,
)
from .models import Student

PAGE_SIZE = 5  # records per page on the students list


def home(request):
    """Send visitors to the dashboard (login_required bounces them to login)."""
    return redirect("dashboard")


# ----------------------------- Authentication -----------------------------
def signup_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account created! Please log in.")
        return redirect("login")
    return render(request, "students/signup.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = LoginForm(request.POST or None)
    next_url = request.POST.get("next") or request.GET.get("next", "")
    if request.method == "POST" and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data["identifier"],
            password=form.cleaned_data["password"],
        )
        if user is None:
            form.add_error(None, "Invalid username/email or password.")
        else:
            login(request, user)
            # Remember me: keep session 2 weeks; otherwise end when browser closes
            request.session.set_expiry(60 * 60 * 24 * 14 if form.cleaned_data["remember_me"] else 0)
            if next_url and url_has_allowed_host_and_scheme(
                next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
            ):
                return redirect(next_url)
            return redirect("dashboard")
    return render(request, "students/login.html", {"form": form, "next": next_url})


@require_POST  # logging out changes state, so only accept POST (with CSRF token)
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")


# -------------------------------- Dashboard --------------------------------
@login_required
def dashboard(request):
    week_ago = timezone.now() - timedelta(days=7)
    context = {
        "total": Student.objects.count(),
        "active": Student.objects.filter(status="active").count(),
        "new": Student.objects.filter(created_at__gte=week_ago).count(),
        "inactive": Student.objects.filter(status="inactive").count(),
    }
    return render(request, "students/dashboard.html", context)


# --------------------------------- Students ---------------------------------
@login_required
def add_student(request):
    form = StudentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        student = form.save()
        messages.success(request, f"{student.full_name} was added successfully.")
        return redirect("view_students")
    return render(request, "students/add_student.html", {"form": form})


@login_required
def view_students(request):
    query = request.GET.get("q", "").strip()
    students = Student.objects.all()
    if query:
        students = students.filter(
            Q(full_name__icontains=query)
            | Q(roll_number__icontains=query)
            | Q(email__icontains=query)
        )
    page = Paginator(students, PAGE_SIZE).get_page(request.GET.get("page"))
    return render(request, "students/view_students.html", {"page": page, "query": query})


@login_required
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)  # pre-filled
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"{student.full_name} was updated.")
        return redirect("view_students")
    return render(request, "students/edit_student.html", {"form": form, "student": student})


@login_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":  # the confirmation page submits a POST
        name = student.full_name
        student.delete()
        messages.success(request, f"{name} was deleted.")
        return redirect("view_students")
    return render(request, "students/delete_student.html", {"student": student})


# --------------------------------- Profile ---------------------------------
@login_required
def profile(request):
    user = request.user
    profile_form = ProfileForm(user, initial={
        "full_name": user.get_full_name(), "username": user.username, "email": user.email,
    })
    password_form = StyledPasswordChangeForm(user)

    if request.method == "POST":
        if request.POST.get("action") == "profile":
            profile_form = ProfileForm(user, request.POST)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Profile updated.")
                return redirect("profile")
        elif request.POST.get("action") == "password":
            password_form = StyledPasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, user)  # keep the user logged in
                messages.success(request, "Password changed.")
                return redirect("profile")

    return render(request, "students/profile.html", {
        "profile_form": profile_form, "password_form": password_form,
    })
