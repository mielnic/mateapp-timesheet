from django.contrib import admin
from .models import Company, Time, Project

# Register your models here.

admin.site.register(Time)
admin.site.register(Company)
admin.site.register(Project)
