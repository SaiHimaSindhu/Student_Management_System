"""Custom login backend: lets users sign in with username OR email."""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None
        User = get_user_model()
        user = User.objects.filter(
            Q(username__iexact=username) | Q(email__iexact=username)
        ).first()
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
