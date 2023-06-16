from .models import Company, Project, Time
from django.contrib.auth import get_user_model

timesheet_queryset = Time.objects.filter(deleted=False).order_by('-timeDate')
print(timesheet_queryset)