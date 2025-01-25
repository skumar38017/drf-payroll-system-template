# salary/backends.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAuthenticationBackend(ModelBackend):
    """
    Custom backend to allow multiple logins (e.g., admin and normal user).
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username=username, password=password, **kwargs)
        if user:
            if user.is_superuser:
                session_key = f"admin_session_{user.pk}"
                request.session[session_key] = True  # Separate session for admin users
            else:
                session_key = f"user_session_{user.pk}"
                request.session[session_key] = True  # Separate session for normal users
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
