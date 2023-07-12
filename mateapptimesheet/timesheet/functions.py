from .models import Company, Project, Time
from django.contrib.auth import get_user_model
from django.db.models import Sum, Q, F, Case, When, Value, IntegerField
import datetime

def monthRewind(firstMonth, a): 
        firstDay = firstMonth.replace(day=1)
        firstMonth = firstDay - datetime.timedelta(days=1)
        if a == 0:
            return firstMonth
        else:
            return monthRewind(firstMonth, a-1)

def updateMaxAllocMonths():
    l = get_user_model().objects.count()
    today = datetime.date.today()
    for i in range(1,l+1):
        user = get_user_model().objects.get(id=i)
        joined = user.date_joined.date()
        months = ((today.year - joined.year) * 12 + (today.month - joined.month))
        if months > 0:
            user.maxAllocMonths = months
        else:
            user.maxAllocMonths = 1
        user.save()

def updateProjectAge():
    l = Project.objects.count()
    today = datetime.date.today()
    for i in range(1, l+1):
        project = Project.objects.get(id=i)
        months = ((today.year - project.startDate.year) * 12 + (today.month - project.startDate.month))
        project.projectAge = months
        project.save()

def timeRange(c):
    todayDate = datetime.date.today()
    monthFirst = todayDate.replace(day = 1)

    if c == 'Current_Month':
        end = todayDate
        start = monthFirst
        ind_alloc_target = 1
    elif c == 'Last_Month':
        end = monthFirst
        start = monthRewind(todayDate, 1)
        ind_alloc_target = 1
    elif c == 'Last_Trimester':
        end = monthFirst
        start = monthRewind(todayDate, 3)
        ind_alloc_target = 3
    elif c == 'Last_Semester':
        end = monthFirst
        start = monthRewind(todayDate, 6)
        ind_alloc_target = 6
    elif c == 'Last_Year':
        end = monthFirst
        start = monthRewind(todayDate, 12)
        ind_alloc_target = 12
    else:
        end = todayDate
        start = datetime.date(1900, 1, 1)
        ind_alloc_target = 1920

    return start, end, ind_alloc_target

def timesheetDateFilter(f):
    start, end, target = timeRange(f)
    timesheet_list = Time.objects.filter(deleted=False, timeDate__gte=start, timeDate__lte=end).order_by('-timeDate')
    return timesheet_list

def timeSum(timesheets_list):
    l = len(timesheets_list)
    s = 0
    for i in range(l):
        s = s + int(timesheets_list[i].timeItem)
    return s

def userAllocTime(f):
    updateMaxAllocMonths()
    start, end, target = timeRange(f)
    user_dataset = get_user_model().objects.order_by('last_name').annotate(
        alloc_time_sum = Sum("time__timeItem", filter=Q(time__deleted=False, time__timeDate__gte=start, time__timeDate__lte=end))
        ).annotate(alloc_time = Case(
            When(alloc_time_sum = None, then = Value(0, output_field=IntegerField())), default='alloc_time_sum'
            )
        ).annotate(range_alloc_target = target * F('allocTarget')
        ).annotate(user_max_alloc_target = F('maxAllocMonths') * F('allocTarget')
        ).annotate(target = Case (
            When(range_alloc_target__gt=F('user_max_alloc_target'), then='user_max_alloc_target'),
            default='range_alloc_target'
             )
        ).annotate(unalloc_time = F('target') - F('alloc_time')
        )
    return user_dataset

def getProjectList():
    updateProjectAge()
    start, end, target = timeRange('Current_Month')
    project_dataset = Project.objects.order_by('projectName').filter(deleted=False
        ).annotate(total_alloc_time_sum=Sum('time__timeItem', filter=Q(time__deleted=False))
        ).annotate(month_alloc_time_sum=Sum('time__timeItem', filter=Q(time__deleted=False, time__timeDate__gte=start, time__timeDate__lte=end))
        ).annotate(total_alloc_time = Case(
            When(total_alloc_time_sum = None, then = Value(0, output_field=IntegerField())), default='total_alloc_time_sum'
            )
        ).annotate(month_alloc_time = Case(
            When(month_alloc_time_sum = None, then = Value(0, output_field=IntegerField())), default='month_alloc_time_sum'
            )
        ).annotate(alloc_time = Case(
            When(projectType='onetime', then='total_alloc_time'), default='month_alloc_time'
            )
        ).annotate(unalloc_time = Case(
            When(projectStatus=True, then=F('budget') - F('alloc_time')), default=0
            )
        ).annotate(balance = Case(
            When(projectType='recurrent', then=(F('budget') * F('projectAge')) - (F('total_alloc_time') - F('month_alloc_time'))), default=F('budget') - F('alloc_time')
            )
        )
    return project_dataset

def getProjectTimesheets(f, pid):
    start, end, target = timeRange(f)
    timesheet_dataset = Time.objects.filter(deleted=False, timeDate__gte=start, timeDate__lte=end, project_id=pid).order_by('-timeDate')
    return timesheet_dataset