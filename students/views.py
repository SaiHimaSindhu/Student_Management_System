from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import StudentForm, StudentSearchForm
from .models import Student


def home(request):
    """
    Landing / dashboard page. Shows quick stats (total students,
    number of courses represented) so it feels like a real dashboard
    rather than a static welcome screen.
    """
    total_students = Student.objects.count()
    total_courses = (
        Student.objects.values_list('course', flat=True).distinct().count()
    )
    recent_students = Student.objects.all()[:5]

    context = {
        'total_students': total_students,
        'total_courses': total_courses,
        'recent_students': recent_students,
    }
    return render(request, 'students/home.html', context)


def about(request):
    """Simple static About page describing the project."""
    return render(request, 'students/about.html')


def add_student(request):
    """
    Create a new Student record. On GET, shows a blank form. On POST,
    validates and saves the form, then redirects to the student list
    (redirect-after-POST avoids duplicate submissions on refresh).
    """
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            messages.success(
                request,
                f'Student "{student.student_name}" was added successfully.'
            )
            return redirect('students:student_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentForm()

    return render(request, 'students/add_student.html', {'form': form})


def student_list(request):
    """
    Display every student in a table, with an optional search box
    that filters by student name OR roll number (case-insensitive).
    """
    search_form = StudentSearchForm(request.GET or None)
    students = Student.objects.all()

    query = ''
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query', '').strip()
        if query:
            students = students.filter(
                Q(student_name__icontains=query) |
                Q(roll_number__icontains=query)
            )

    context = {
        'students': students,
        'search_form': search_form,
        'query': query,
        'total_results': students.count(),
    }
    return render(request, 'students/student_list.html', context)


def edit_student(request, pk):
    """Update an existing Student, identified by primary key `pk`."""
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f'Student "{student.student_name}" was updated successfully.'
            )
            return redirect('students:student_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentForm(instance=student)

    return render(
        request,
        'students/edit_student.html',
        {'form': form, 'student': student}
    )


def delete_student(request, pk):
    """
    Show a confirmation page before deleting (GET), then actually
    delete the record once the user confirms (POST). This two-step
    flow prevents accidental deletion from a single click / link.
    """
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        name = student.student_name
        student.delete()
        messages.success(request, f'Student "{name}" was deleted.')
        return redirect('students:student_list')

    return render(
        request,
        'students/delete_confirm.html',
        {'student': student}
    )
