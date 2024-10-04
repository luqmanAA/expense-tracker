from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):

    def create_user(self, email, password=None, **extra_fields):
        username = email
        return super().create_user(username, email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        username = email
        return super().create_superuser(username, email, password, **extra_fields)
