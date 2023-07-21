from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailAuthenticationBackend(ModelBackend):
    def authenticate(self, request, email, password, **kwargs):
        User = get_user_model()

        if not email or not password:
            return None

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None
