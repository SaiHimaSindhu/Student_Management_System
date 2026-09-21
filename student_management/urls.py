"""
URL configuration for the student_management project.

This file only wires up two things:
1. The Django admin site.
2. The `students` app's own urls.py (which contains all the actual
   pages: home, add student, student list, edit, delete, about).

Media files (uploaded profile photos) are served by Django's dev
server only while DEBUG=True. In production you would serve them via
your web server (nginx/Apache) or a storage service instead.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('students.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
