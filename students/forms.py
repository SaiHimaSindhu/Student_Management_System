"""Forms: validation lives here so the views stay small."""
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import Student

User = get_user_model()


class StyledFormMixin:
    """Adds our CSS class to every input so templates stay simple."""

    def style_fields(self):
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("class", "form-input")


# ----------------------------- Authentication -----------------------------
class SignupForm(StyledFormMixin, forms.Form):
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    username = forms.CharField(max_length=150)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_fields()

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"].strip()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get("password1"), cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Passwords do not match.")
        elif p1:
            try:
                validate_password(p1)
            except ValidationError as error:
                self.add_error("password1", error)
        return cleaned

    def save(self):
        first, _, last = self.cleaned_data["full_name"].strip().partition(" ")
        return User.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password1"],
            first_name=first,
            last_name=last,
        )


class LoginForm(StyledFormMixin, forms.Form):
    identifier = forms.CharField(label="Email or Username")
    password = forms.CharField(widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False, label="Remember me")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_fields()


# -------------------------------- Students --------------------------------
class StudentForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "full_name", "roll_number", "email", "phone_number",
            "course", "year", "status", "address",
        ]
        widgets = {"address": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_fields()
        self.fields["year"].choices = [("", "Select year")] + Student.YEAR_CHOICES

    def clean_roll_number(self):
        return self.cleaned_data["roll_number"].strip()


# --------------------------------- Profile --------------------------------
class ProfileForm(StyledFormMixin, forms.Form):
    full_name = forms.CharField(max_length=100)
    username = forms.CharField(max_length=150)
    email = forms.EmailField()

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.style_fields()

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if User.objects.filter(username__iexact=username).exclude(pk=self.user.pk).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"].strip()
        if User.objects.filter(email__iexact=email).exclude(pk=self.user.pk).exists():
            raise ValidationError("This email is used by another account.")
        return email

    def save(self):
        first, _, last = self.cleaned_data["full_name"].strip().partition(" ")
        self.user.first_name, self.user.last_name = first, last
        self.user.username = self.cleaned_data["username"]
        self.user.email = self.cleaned_data["email"]
        self.user.save()
        return self.user


class StyledPasswordChangeForm(StyledFormMixin, PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_fields()
