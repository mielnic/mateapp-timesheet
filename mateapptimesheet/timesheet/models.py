from datetime import date
from django.db import models
from django.conf import settings
from .validators import invalidate_future_timesheets

# Create your models here.

class BaseModel(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class Address(BaseModel):
    street = models.CharField(max_length=200, blank=True)
    postalCode = models.CharField(max_length=7, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    deleted = models.BooleanField(blank=True, default=0)
    deletedBy = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.street}, {self.city}'

class Company(BaseModel):
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

class Project(BaseModel):
    projectName = models.CharField(max_length=100, blank=True)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, blank=True, null=True)
    projectStatus = models.BooleanField(blank=True, default=1)
    projectType = models.CharField(max_length=15, blank=True)
    budget = models.IntegerField(default=0, blank=True)
    startDate = models.DateField(blank=False, null=True, default=date.today)
    projectAge = models.IntegerField(default=0, blank=True)
    projectNotes = models.CharField(max_length=500, blank=True)
    deleted = models.BooleanField(blank=True, default=0)
    deletedBy = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.projectName} - {self.company}'
    
class Time(BaseModel):
    timeItem = models.IntegerField(blank=False, null=True)
    timeDate = models.DateField(blank=False, null=True, default=date.today, validators=[invalidate_future_timesheets])
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, blank=True, null=True)
    timeType = models.CharField(max_length=100, blank=True)
    timeRevenue = models.BooleanField(blank=True, default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True)
    timeNotes = models.CharField(max_length=500, blank=True)
    deleted = models.BooleanField(blank=True, default=0)
    deletedBy = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.timeDate}, {self.project}, {self.user}'
