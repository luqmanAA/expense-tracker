from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.managers import CustomUserManager
from base.models import BaseModel


# Create your models here.


class Role(BaseModel):
    name = models.CharField(max_length=200)

    class Meta:
        indexes = [
            models.Index(fields=(
                'name',
            )),
        ]

    def __str__(self):
        return self.name


class User(BaseModel, AbstractUser):
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    email = models.EmailField(_('email address'), max_length=150, unique=True)
    middle_name = models.CharField(max_length=200, null=True, blank=True)
    roles = models.ForeignKey('Role', on_delete=models.CASCADE, related_name="users")
    subsidiary = models.ForeignKey('organization.Subsidiary', on_delete=models.SET_NULL, null=True, blank=True)
    department = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        indexes = [
            models.Index(fields=(
                'email',
                'created_at',
            )),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
