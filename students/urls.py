from django.urls import path

from . import views

app_name = 'students'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/<int:pk>/edit/', views.edit_student, name='edit_student'),
    path('students/<int:pk>/delete/', views.delete_student, name='delete_student'),
]
