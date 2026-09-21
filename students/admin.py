from django.contrib import admin

from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'student_name', 'roll_number', 'email', 'phone',
        'course', 'gender', 'joining_date',
    )
    list_filter = ('course', 'gender')
    search_fields = ('student_name', 'roll_number', 'email')
    ordering = ('-created_at',)
