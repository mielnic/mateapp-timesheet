from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .validators import validate_email_domain
from .managers import CustomUserManager
from datetime import date


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True, validators=[validate_email_domain])
    seniority = models.CharField(max_length=15, blank=True)
    practice = models.CharField(max_length=20, blank=True)
    title = models.CharField(max_length=50, blank=True)
    allocTarget = models.IntegerField(default=160, blank=True)
    maxAllocMonths = models.IntegerField(default=0, blank=True)
    startDate = models.DateField(blank=False, null=True, default=date.today)
    role = models.CharField(max_length=15, default='User', blank=True, null=True)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
