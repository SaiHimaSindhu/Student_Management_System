from django import forms

from .models import Student


class StudentForm(forms.ModelForm):
    """
    ModelForm used for both creating and updating a Student.

    Bootstrap classes are applied to every widget via the Meta.widgets
    dictionary so the rendered form matches the rest of the UI without
    needing extra template filters.
    """

    class Meta:
        model = Student
        fields = [
            'student_name',
            'roll_number',
            'email',
            'phone',
            'course',
            'gender',
            'address',
            'profile_photo',
            'joining_date',
        ]
        widgets = {
            'student_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name',
            }),
            'roll_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. CS-2024-001',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'student@example.com',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. +919876543210',
            }),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Residential address',
            }),
            'profile_photo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'joining_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }

    def clean_roll_number(self):
        """
        Extra, form-level uniqueness check so we can show a friendly
        error message next to the field instead of an ugly database
        IntegrityError. Works correctly for both create (no instance
        yet) and update (exclude the current instance from the check).
        """
        roll_number = self.cleaned_data['roll_number'].strip()
        qs = Student.objects.filter(roll_number__iexact=roll_number)

        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(
                'A student with this roll number already exists.'
            )
        return roll_number

    def clean_student_name(self):
        name = self.cleaned_data['student_name'].strip()
        if not name:
            raise forms.ValidationError('Student name is required.')
        return name


class StudentSearchForm(forms.Form):
    """Simple search-by-name-or-roll-number form used on the list page."""
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name or roll number...',
        })
    )
