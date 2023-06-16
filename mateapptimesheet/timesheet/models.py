from datetime import date
from django.db import models
from django.conf import settings

# Create your models here.

class Address(models.Model):
    street = models.CharField(max_length=200, blank=True)
    postalCode = models.CharField(max_length=7, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    deleted = models.BooleanField(blank=True, default=0)
    deletedBy = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.street}, {self.city}'

class Company(models.Model):
    companyName = models.CharField(max_length=100, blank=True)
    tax_id = models.CharField(max_length=15, blank=True)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True)
    companyPhone = models.CharField(max_length=25, blank=True)
    companyNotes = models.CharField(max_length=500, blank=True)
    deleted = models.BooleanField(blank=True, default=0)
    deletedBy = models.BigIntegerField(blank=True, null=True)
    
    def __str__(self):
        return self.companyName

class Project(models.Model):
    projectName = models.CharField(max_length=100, blank=True)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, blank=True, null=True)
    projectStatus = models.BooleanField(blank=True, default=0)
    projectType = models.CharField(max_length=15, blank=True)
    deleted = models.BooleanField(blank=True, default=0)
    deletedBy = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return self.projectName
    
class Time(models.Model):
    timeItem = models.IntegerField(blank=False, null=True)
    timeDate = models.DateField(blank=False, null=True, default=date.today)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, blank=True, null=True)
    timeType = models.CharField(max_length=100, blank=True)
    timeRevenue = models.BooleanField(blank=True, default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True)
    timeNotes = models.CharField(max_length=500, blank=True)
    deleted = models.BooleanField(blank=True, default=0)
    deletedBy = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.timeDate}, {self.project}, {self.user}'
