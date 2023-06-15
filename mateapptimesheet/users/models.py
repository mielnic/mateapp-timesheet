from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .validators import validate_email_domain
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True, validators=[validate_email_domain])
    seniority = models.CharField(max_length=10, blank=True)
    practice = models.CharField(max_length=20, blank=True)
    title = models.CharField(max_length=50, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
