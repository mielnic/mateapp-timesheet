from .models import Company, Project, Time
from django.contrib.auth import get_user_model
import datetime

def timeRange(c):
    todayDate = datetime.date.today()
    if c == 'Current_Month':
        end = todayDate
        start = todayDate.replace(day = 1)
    elif c == 'Last_Month':
        pass
    


timesheet_queryset = Time.objects.filter(deleted=False).order_by('-timeDate')
print(timesheet_queryset)