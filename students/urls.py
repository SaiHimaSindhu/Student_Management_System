"""URL routes for the students app."""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("students/", views.view_students, name="view_students"),
    path("students/add/", views.add_student, name="add_student"),
    path("students/<int:pk>/edit/", views.edit_student, name="edit_student"),
    path("students/<int:pk>/delete/", views.delete_student, name="delete_student"),
    path("profile/", views.profile, name="profile"),
]
