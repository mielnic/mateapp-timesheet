from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, response, request
from django.template import loader
from django.contrib import messages
from .models import Address, Company, Project, Time
from .forms import CompanyForm, ProjectForm, TimesheetForm, FilterForm
from .functions import timeRange, timeSum
from main.forms import SearchForm
from main.functions import paginator
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from main.decorators import user_not_authenticated, allowed_users
from django.contrib.auth import get_user_model
import datetime
from itertools import chain
from operator import attrgetter




# CRUD Customer (Staff CUD)

# Customer List

@login_required
def companies(request, a, b):
    searchform = SearchForm
    if 'q' in request.GET:
        searchform = SearchForm(request.GET)
        if searchform.is_valid():
            q = searchform.cleaned_data['q']
            companies_list = Company.objects.filter(companyName__icontains=q, deleted=False)
            links, idxPL, idxPR, idxNL, idxNR = '', '', '', '', ''
            template = loader.get_template('timesheet/company_list.html')
            if not companies_list:
                messages.warning(request, _("The search didn't return any result."))

    else:
        companies_list = Company.objects.order_by('companyName').filter(deleted=False) [a:b]
        length = Company.objects.filter(deleted=False).count()
        links, idxPL, idxPR, idxNL, idxNR = paginator(a, length, 10)
        template = loader.get_template('timesheet/company_list.html')

    context = {
        'companies_list': companies_list,
        'searchform' : searchform,
        'links' : links,
        'idxPL' : idxPL,
        'idxPR' : idxPR,
        'idxNL' : idxNL,
        'idxNR' : idxNR,
    }
    return HttpResponse(template.render(context, request))

# Customer View

@login_required
def company(request, id, a, b):
    company = Company.objects.get(id=id)
    project_list = Project.objects.filter(company_id=id).filter(deleted=False) [a:b]
    length = Project.objects.filter(company_id=id).filter(deleted=False).count()
    links, idxPL, idxPR, idxNL, idxNR = paginator(a, length, 5)
    template = loader.get_template('timesheet/company_view.html')
    context = {
        'company' : company,
        'project_list' : project_list,
        'links' : links,
        'idxPL' : idxPL,
        'idxPR' : idxPR,
        'idxNL' : idxNL,
        'idxNR' : idxNR,
    }
    return HttpResponse(template.render(context, request))


# Customer Create

@login_required
@allowed_users(allowed_roles=['admin', 'staff'])
def create_company(request):
    if request.method == 'POST':
        companyform = CompanyForm(request.POST)
        if companyform.is_valid():
            companyform.save()
            id = Company.objects.last().id
            return HttpResponseRedirect(f'/timesheet/company/{id}/0/5/')     

    else:
        companyform = CompanyForm()

    context = {
        'companyform': companyform,
        'title': _("New Customer")
    }
    return render(request, 'timesheet/company_create.html', context)

# Customer Update

@login_required
@allowed_users(allowed_roles=['admin', 'staff'])
def edit_company(request, id):
    company = Company.objects.get(id=id)
    companyform = CompanyForm(request.POST or None, instance=company)
    if companyform.is_valid():
        companyform.save()
        return HttpResponseRedirect(f'/timesheet/company/{id}/0/5/')
    
    context = {
        'companyform': companyform,
        'company' : company,
    }
    return render(request, 'timesheet/company_create.html', context)

# Customer Delete

@login_required
@allowed_users(allowed_roles=['admin', 'staff'])
def delete_company(request, id):
    uid = request.user.id
    company = Company.objects.get(id=id)
    company.deleted = 1
    company.deletedBy = uid
    company.save()
    return redirect('/timesheet/companies/0/10/')

# Customer Restore

@login_required
@allowed_users(allowed_roles=['admin', 'staff'])
def restore_company(request, id, u):
    company = Company.objects.get(id=id)
    company.deleted = 0
    company.save()
    if u == 0:
        return redirect('/user_trash/0/10/')
    else:
        return redirect('/admin_trash/0/10/')

# Customer Full Delete

@login_required
@allowed_users(allowed_roles=['admin', 'staff'])
def full_delete_company(request, id):
    company = Company.objects.get(id=id)
    company.deletedBy = None
    company.save()
    return redirect('/user_trash/0/10/')

# CRUD Project (Staff CUD)

# Project List

@login_required
def projects(request, a, b):
    searchform = SearchForm
    if 'q' in request.GET:
        searchform = SearchForm(request.GET)
        if searchform.is_valid():
            q = searchform.cleaned_data['q']
            projects_list = Project.objects.filter(projectName__icontains=q, deleted=False)
            links, idxPL, idxPR, idxNL, idxNR = '', '', '', '', ''
            template = loader.get_template('timesheet/project_list.html')
            if not projects_list:
                messages.warning(request, _("The search didn't return any result."))

    else:
        projects_list = Project.objects.order_by('projectName').filter(deleted=False) [a:b]
        length = Project.objects.filter(deleted=False).count()
        links, idxPL, idxPR, idxNL, idxNR = paginator(a, length, 10)
        template = loader.get_template('timesheet/project_list.html')

    context = {
        'projects_list': projects_list,
        'searchform' : searchform,
        'links' : links,
        'idxPL' : idxPL,
        'idxPR' : idxPR,
        'idxNL' : idxNL,
        'idxNR' : idxNR,
    }
    return HttpResponse(template.render(context, request))

# Project View

@login_required
def project(request, id, a, b):
    project = Project.objects.get(id=id)
    timesheet_list = Time.objects.filter(project_id=id, deleted=False).order_by('-timeDate') [a:b]
    length = Time.objects.filter(project_id=id).filter(deleted=False).count()
    links, idxPL, idxPR, idxNL, idxNR = paginator(a, length, 5)
    template = loader.get_template('timesheet/project_view.html')
    context = {
        'project' : project,
        'timesheet_list' : timesheet_list,
        'links' : links,
        'idxPL' : idxPL,
        'idxPR' : idxPR,
        'idxNL' : idxNL,
        'idxNR' : idxNR,
    }
    return HttpResponse(template.render(context, request))

# Project Create

@login_required
@allowed_users(allowed_roles=['admin', 'staff'])
def create_project(request):
    if request.method == 'POST':
        projectform = ProjectForm(request.POST)
        if projectform.is_valid():
            projectform.save()
            id = Project.objects.last().id
            return HttpResponseRedirect(f'/timesheet/project/{id}/0/5/')     

    else:
        projectform = ProjectForm()

    context = {
        'projectform': projectform,
        'title': _("New Project")
    }
    return render(request, 'timesheet/project_create.html', context)

# Project Update

@login_required
@allowed_users(allowed_roles=['admin', 'staff'])
def edit_project(request, id):
    project = Project.objects.get(id=id)
    projectform = ProjectForm(request.POST or None, instance=project)
    if projectform.is_valid():
        projectform.save()
        return HttpResponseRedirect(f'/timesheet/project/{id}/0/5/')
    
    context = {
        'projectform': projectform,
        'project' : project,
    }
    return render(request, 'timesheet/project_create.html', context)

# Project Delete

@login_required
@allowed_users(allowed_roles=['admin', 'staff'])
def delete_project(request, id):
    uid = request.user.id
    project = Project.objects.get(id=id)
    project.deleted = 1
    project.deletedBy = uid
    project.save()
    return redirect('/timesheet/projects/0/10/')

# Project Restore

@login_required
@allowed_users(allowed_roles=['admin', 'staff'])
def restore_project(request, id, u):
    project = Project.objects.get(id=id)
    project.deleted = 0
    project.save()
    if u == 0:
        return redirect('/user_trash/0/10/')
    else:
        return redirect('/admin_trash/0/10/')

# Project Full Delete

@login_required
@allowed_users(allowed_roles=['admin', 'staff'])
def full_delete_project(request, id):
    project = Project.objects.get(id=id)
    project.deletedBy = None
    project.save()
    return redirect('/user_trash/0/10/')

# CRUD Time Item (User)

# Timesheet List

@login_required
def timesheets(request, a, b):
    searchform = SearchForm
    if 'q' in request.GET:
        searchform = SearchForm(request.GET)
        if searchform.is_valid():
            print('valid q!')
            q = searchform.cleaned_data['q']
            project_list = Time.objects.filter(project__projectName__icontains=q, deleted=False)
            user_fn_list = Time.objects.filter(user__last_name__icontains=q, deleted=False)
            user_ln_list = Time.objects.filter(user__first_name__icontains=q, deleted=False)
            timesheets_list = sorted(chain(project_list, user_ln_list, user_fn_list),
                                     key=attrgetter('timeDate'),
                                     reverse=True,
                                     )
            print(len(timesheets_list))
            print(timesheets_list[2].timeItem,)
            links, idxPL, idxPR, idxNL, idxNR = '', '', '', '', ''
            template = loader.get_template('timesheet/timesheet_list.html')
            if not timesheets_list:
                messages.warning(request, _("The search didn't return any result."))

    else:
        timesheets_list = Time.objects.order_by('-timeDate').filter(deleted=False) [a:b]
        length = Time.objects.filter(deleted=False).count()
        links, idxPL, idxPR, idxNL, idxNR = paginator(a, length, 10)
        template = loader.get_template('timesheet/timesheet_list.html')

    context = {
        'timesheets_list': timesheets_list,
        'searchform' : searchform,
        'links' : links,
        'idxPL' : idxPL,
        'idxPR' : idxPR,
        'idxNL' : idxNL,
        'idxNR' : idxNR,
    }
    return HttpResponse(template.render(context, request))

# Timesheet List Self

@login_required
def self_timesheets(request, a, b):
    id = request.user.id
    user = get_user_model().objects.get(id=id)
    filterform = FilterForm
    s = ''
    if 'q' in request.GET or 'f' in request.GET:
        filterform = FilterForm(request.GET)
        if filterform.is_valid():   
            f = filterform.cleaned_data['f']
            timesheets_list = timeRange(f)
            if 'q' in request.GET:
                if filterform.is_valid():
                    q = filterform.cleaned_data['q']
                    timesheets_list = timesheets_list.filter(project__projectName__icontains=q, deleted=False)
            links, idxPL, idxPR, idxNL, idxNR = '', '', '', '', ''
            template = loader.get_template('timesheet/timesheet_list_self.html')
            s = timeSum(timesheets_list)
            if not timesheets_list:
                messages.warning(request, _("The search didn't return any result."))

    else:
        print('standard!')
        timesheets_list = Time.objects.order_by('-timeDate').filter(user=user, deleted=False) [a:b]
        length = Time.objects.filter(user=user, deleted=False).count()
        links, idxPL, idxPR, idxNL, idxNR = paginator(a, length, 10)
        template = loader.get_template('timesheet/timesheet_list_self.html')

    context = {
        'timesheets_list': timesheets_list,
        'filterform' : filterform,
        's' : s,
        'links' : links,
        'idxPL' : idxPL,
        'idxPR' : idxPR,
        'idxNL' : idxNL,
        'idxNR' : idxNR,
    }
    return HttpResponse(template.render(context, request))

# Timesheet View

@login_required
def timesheet(request, id):
    timesheet = Time.objects.get(id=id)
    template = loader.get_template('timesheet/timesheet_view.html')
    context = {
        'timesheet' : timesheet,
    }
    return HttpResponse(template.render(context, request))

# Timesheet View Self

@login_required
def timesheet_self(request, id):
    timesheet = Time.objects.get(id=id)
    template = loader.get_template('timesheet/timesheet_view_self.html')
    context = {
        'timesheet' : timesheet,
    }
    return HttpResponse(template.render(context, request))


# Timesheet Create

@login_required
@allowed_users(allowed_roles=['admin', 'staff'])
def create_timesheet(request):
    if request.method == 'POST':
        timesheetform = TimesheetForm(request.POST)
        if timesheetform.is_valid():
            timesheetform.save()
            id = Time.objects.last().id
            return HttpResponseRedirect('/timesheet/timesheets/0/10/')     

    else:
        timesheetform = TimesheetForm()

    context = {
        'timesheetform': timesheetform,
        'title': _("Log Timesheet")
    }
    return render(request, 'timesheet/timesheet_create.html', context)

# Timesheet Create self

@login_required
def create_self_timesheet(request):
    id = request.user.id
    user = get_user_model().objects.get(id=id)
    if request.method == 'POST':
        timesheetform = TimesheetForm(request.POST)
        if timesheetform.is_valid():
            timesheetform.save()
            id = Time.objects.last().id
            timesheet = Time.objects.get(id=id)
            timesheet.user = user
            timesheet.save()
            return HttpResponseRedirect('/timesheet/timesheets_self/0/10/')

    else:
        timesheetform = TimesheetForm()

    context = {
        'timesheetform': timesheetform,
        'title': _("Log Timesheet")
    }
    return render(request, 'timesheet/timesheet_create_self.html', context)


# Timesheet Update

@login_required
def edit_timesheet(request, id):
    timesheet = Time.objects.get(id=id)
    timesheetform = TimesheetForm(request.POST or None, instance=timesheet)
    if timesheetform.is_valid():
        timesheetform.save()
        return HttpResponseRedirect('/timesheet/timesheets/0/10/')
    
    context = {
        'timesheetform': timesheetform,
        'timesheet' : timesheet,
    }
    return render(request, 'timesheet/timesheet_create.html', context)

# Timesheet Update Self

@login_required
def edit_self_timesheet(request, id):
    uid = request.user.id
    user = get_user_model().objects.get(id=uid)
    timesheet = Time.objects.get(id=id)
    timesheetform = TimesheetForm(request.POST or None, instance=timesheet)
    if timesheetform.is_valid():
        timesheetform.save()
        timesheet.user = user
        timesheet.save()
        return HttpResponseRedirect('/timesheet/timesheets_self/0/10/')
    
    context = {
        'timesheetform': timesheetform,
        'timesheet' : timesheet,
    }
    return render(request, 'timesheet/timesheet_create_self.html', context)

# Timesheet Delete

@login_required
def delete_timesheet(request, id, u):
    uid = request.user.id
    timesheet = Time.objects.get(id=id)
    timesheet.deleted = 1
    timesheet.deletedBy = uid
    timesheet.save()
    if u == 0:
        return redirect('/timesheet/timesheets_self/0/10/')
    else:
        return redirect('/timesheet/timesheets/0/10/')

# Timesheet Restore

@login_required
def restore_timesheet(request, id, u):
    timesheet = Time.objects.get(id=id)
    timesheet.deleted = 0
    timesheet.save()
    if u == 0:
        return redirect('/user_trash/0/10/')
    else:
        return redirect('/admin_trash/0/10/')

# Timesheet Full Delete

@login_required
def full_delete_timesheet(request, id):
    timesheet = Time.objects.get(id=id)
    timesheet.deletedBy = None
    timesheet.save()
    return redirect('/user_trash/0/10/')



# View Project (users w/sumarized time?)

# View Users (projects w/sumarized time?)

def dev_button(request):
    dateref = datetime.datetime(2023, 6, 15)
    timesheets_list = Time.objects.order_by('-timeDate').filter(deleted=False, timeDate__lt=dateref)
    timesheets_list=list(timesheets_list)
    print(timesheets_list)
    return redirect('/timesheet/timesheets/0/10/')