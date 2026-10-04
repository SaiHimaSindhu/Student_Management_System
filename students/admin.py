from django.contrib import admin

from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "roll_number", "email", "course", "year", "status")
    list_filter = ("status", "year", "course")
    search_fields = ("full_name", "roll_number", "email")
