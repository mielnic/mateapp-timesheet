from .models import Company, Project, Time
from django.contrib.auth import get_user_model
import datetime

def timeRange(c):
    todayDate = datetime.date.today()
    monthFirst = todayDate.replace(day = 1)

    def monthRewind(firstMonth, a): 
        firstDay = firstMonth.replace(day=1)
        firstMonth = firstDay - datetime.timedelta(days=1)
        if a == 0:
            return firstMonth
        else:
            return monthRewind(firstMonth, a-1)

    if c == 'Current_Month':
        end = todayDate
        start = monthFirst
    elif c == 'Last_Month':
        end = monthFirst
        start = monthRewind(todayDate, 1)
    elif c == 'Last_Trimester':
        end = monthFirst
        start = monthRewind(todayDate, 3)
    elif c == 'Last_Semester':
        end = monthFirst
        start = monthRewind(todayDate, 6)
    elif c == 'Last_Year':
        end = monthFirst
        start = monthRewind(todayDate, 12)
    else:
        end = todayDate
        start = datetime.date(1900, 1, 1)

    timesheet_list = Time.objects.filter(deleted=False, timeDate__gte=start, timeDate__lte=end).order_by('-timeDate')
    return timesheet_list

def timeSum(timesheets_list):
    l = len(timesheets_list)
    s = 0
    for i in range(l):
        s = s + int(timesheets_list[i].timeItem)
    return s
