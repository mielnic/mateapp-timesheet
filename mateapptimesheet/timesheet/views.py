from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, response, request, QueryDict
from django.template import loader
from django.contrib import messages
from .models import Address, Company, Project, Time
from .forms import CompanyForm, ProjectForm, TimesheetForm, FilterForm, TimeNotesForm, CompanyNotesForm, ProjectNotesForm
from .functions import timeSum, timesheetDateFilter, userAllocTime, getProjectList, getProjectTimesheets, checkProjectEmpty, getUserProjects
from main.forms import SearchForm
from main.functions import paginator
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from main.decorators import allowed_users
from django.contrib.auth import get_user_model
from django.db.models import Sum, Q
from django.contrib.postgres.search import SearchVector, SearchQuery




# CRUD Customer (Staff CUD)

# Customer List

@login_required
@allowed_users(allowed_roles=['admin', 'staff', 'supervisor'])
def companies(request, a, b):
    searchform = SearchForm
    if 'q' in request.GET:
        searchform = SearchForm(request.GET)
        if searchform.is_valid():
            q = searchform.cleaned_data['q']
            companies_list = Company.objects.filter(companyName__icontains=q, deleted=False)
            pgx = ''
            template = loader.get_template('timesheet/company_list.html')

    else:
        companies_list = Company.objects.order_by('companyName').filter(deleted=False) [a:b]
        length = Company.objects.filter(deleted=False).count()
        pgx = paginator(a, length, b)
        template = loader.get_template('timesheet/company_list.html')

    context = {
        'companies_list': companies_list,
        'searchform' : searchform,
        'pgx' : pgx,
    }
    return HttpResponse(template.render(context, request))

# Customer View

@login_required
#@allowed_users(allowed_roles=['admin', 'staff'])
def company(request, id, a, b):
    company = Company.objects.get(id=id)
    project_dataset = getProjectList()
    project_list = project_dataset.filter(company_id=id).order_by('-projectStatus', 'projectName') [a:b]
    total_balance = project_dataset.filter(company_id=id).filter(Q(projectType='recurrent') | Q(projectStatus=False)).aggregate(Sum('balance'))
    length = Project.objects.filter(company_id=id).filter(deleted=False).count()
    pgx = paginator(a, length, b)
    template = loader.get_template('timesheet/company_view.html')
    context = {
        'company' : company,
        'project_list' : project_list,
        'total_balance' : total_balance,
        'pgx' : pgx,
    }
    return HttpResponse(template.render(context, request))


# Customer Create

@login_required
@allowed_users(allowed_roles=['admin', 'staff', 'supervisor'])
def create_company(request):
    if request.method == 'POST':
        companyform = CompanyForm(request.POST)
        if companyform.is_valid():
            company = companyform.save()
            id = company.id
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
@allowed_users(allowed_roles=['admin', 'staff', 'supervisor'])
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
@allowed_users(allowed_roles=['admin', 'staff', 'supervisor'])
def delete_company(request, id):
    uid = request.user.id
    company = Company.objects.get(id=id)
    company.deleted = 1
    company.deletedBy = uid
    company.save()
    return redirect('/timesheet/companies/0/10/')

# Customer Restore

@login_required
@allowed_users(allowed_roles=['admin', 'staff', 'supervisor'])
def restore_company(request, id, u):
    company = Company.objects.get(id=id)
    company.deleted = 0
    company.save()
    return HttpResponse(status = 200)

# Customer Full Delete

@login_required
@allowed_users(allowed_roles=['admin', 'staff', 'supervisor'])
def full_delete_company(request, id):
    company = Company.objects.get(id=id)
    company.deletedBy = None
    company.save()
    return HttpResponse(status = 200)

# CRUD Project (Staff CUD)

# Project List

@login_required
def projects(request, a, b):
    searchform = SearchForm
    if 'q' in request.GET:
        searchform = SearchForm(request.GET)
        if searchform.is_valid():
            q = searchform.cleaned_data['q']
            q = q.lower()
            status = True
            if '@inactive' in q:
                status = False
                q = q.replace('@inactive', '').strip()
                print(q, status)
            project_dataset = getProjectList()
            if q:
                project_list = project_dataset.annotate(search=SearchVector("projectName", "company__companyName")).filter(search=SearchQuery(q), projectStatus=status)
            else:
                project_list = project_dataset.filter(projectStatus=status)
            pgx = ''
            template = loader.get_template('timesheet/project_list.html')
    else:
        project_dataset = getProjectList().filter(projectStatus=True)
        project_list = project_dataset [a:b]
        length = project_dataset.count()
        pgx = paginator(a, length, b)
        template = loader.get_template('timesheet/project_list.html')

    context = {
        'project_list': project_list,
        'searchform' : searchform,
        'pgx' : pgx,
    }
    return HttpResponse(template.render(context, request))

# Project View

@login_required
#@allowed_users(allowed_roles=['admin', 'staff', 'supervisor'])
def project(request, id, a, b):

    project = Project.objects.get(id=id)
    empty = checkProjectEmpty(id)

    if project.projectType == 'onetime':
        user_dataset = getProjectTimesheets('All', project.id)
        filterform = FilterForm(initial={'f':'All'})
        recurrent = False
    else:
        user_dataset = getProjectTimesheets('Current_Month', project.id)
        filterform = FilterForm(initial={'f':'Current_Month'})
        recurrent = True
    
    total_alloc_time = user_dataset.aggregate(Sum('alloc_time'))
    try:
        pending_time = project.budget - (total_alloc_time['alloc_time__sum'])
    except:
        pending_time = project.budget
    
    if 'q' in request.GET or 'f' in request.GET:
        filterform = FilterForm(request.GET)
        if filterform.is_valid():   
            f = filterform.cleaned_data['f']
            q = filterform.cleaned_data['q']
            user_list = getProjectTimesheets(f, project.id)
            if q:       
                user_list = user_list.annotate(search=SearchVector("last_name", "first_name")).filter(search=SearchQuery(q))
            pgx = ''
            template = loader.get_template('timesheet/project_view.html')
            view_total_alloc_time = user_list.aggregate(Sum('alloc_time'))           
    else:
        view_total_alloc_time = total_alloc_time
        user_list = user_dataset [a:b]
        length = user_dataset.count()
        pgx = paginator(a, length, b)
        template = loader.get_template('timesheet/project_view.html')
        
    context = {
        'project' : project,
        'user_list' : user_list,
        'filterform' : filterform,
        'total_alloc_time' : view_total_alloc_time,
        'pending_time' : pending_time,
        'recurrent' : recurrent,
        'empty' : empty,
        'pgx' : pgx,
    }
    return HttpResponse(template.render(context, request))

# Project Create

@login_required
@allowed_users(allowed_roles=['admin', 'staff', 'supervisor'])
def create_project(request):
    if request.method == 'POST':
        projectform = ProjectForm(request.POST)
        if projectform.is_valid():
            project = projectform.save()
            id = project.id
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
@allowed_users(allowed_roles=['admin', 'staff', 'supervisor'])
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
@allowed_users(allowed_roles=['admin', 'staff', 'supervisor'])
def delete_project(request, id):
    uid = request.user.id
    project = Project.objects.get(id=id)
    project.deleted = 1
    project.deletedBy = uid
    project.save()
    return redirect('/timesheet/projects/0/10/')

# Project Restore

@login_required
@allowed_users(allowed_roles=['admin', 'staff', 'supervisor'])
def restore_project(request, id, u):
    project = Project.objects.get(id=id)
    project.deleted = 0
    project.save()
    return HttpResponse(status = 200)

# Project Full Delete

@login_required
@allowed_users(allowed_roles=['admin', 'staff', 'supervisor'])
def full_delete_project(request, id):
    project = Project.objects.get(id=id)
    project.deletedBy = None
    project.save()
    return HttpResponse(status = 200)

# CRUD Time Item (User)

# Timesheet List

@login_required
def timesheets(request, a, b):
    filterform = FilterForm
    s = ''
    if 'q' in request.GET or 'f' in request.GET:
        filterform = FilterForm(request.GET)
        if filterform.is_valid():   
            f = filterform.cleaned_data['f']
            q = filterform.cleaned_data['q']
            timesheets_list = timesheetDateFilter(f)
            if q:
                timesheets_list = timesheets_list.annotate(search=SearchVector("project__projectName", "project__company__companyName", "user__first_name", "user__last_name")).filter(search=SearchQuery(q), deleted=False).order_by('-timeDate')
            pgx = ''
            template = loader.get_template('timesheet/timesheet_list.html')
            s = timeSum(timesheets_list)

    else:
        filterform = FilterForm(initial={'f':'All'})
        timesheets_dataset = timesheetDateFilter('All')
        timesheets_dataset = Time.objects.order_by('-timeDate').filter(deleted=False)
        s = timeSum(timesheets_dataset)
        timesheets_list = timesheets_dataset [a:b]
        length = Time.objects.filter(deleted=False).count()
        pgx = paginator(a, length, b)
        template = loader.get_template('timesheet/timesheet_list.html')

    context = {
        'timesheets_list': timesheets_list,
        'filterform' : filterform,
        's' : s,
        'pgx' : pgx,
    }
    return HttpResponse(template.render(context, request))

# Timesheet List Self

@login_required
def self_timesheets(request, a=0, b=10):
    id = request.user.id
    user = get_user_model().objects.get(id=id)
    filterform = FilterForm
    s = ''
    if 'q' in request.GET or 'f' in request.GET:
        filterform = FilterForm(request.GET)
        if filterform.is_valid():   
            f = filterform.cleaned_data['f']
            q = filterform.cleaned_data['q']
            timesheets_list = timesheetDateFilter(f)
            timesheets_list = timesheets_list.filter(user=user)
            if q:
                timesheets_list = timesheets_list.annotate(search=SearchVector("project__projectName", "project__company__companyName")).filter(search=SearchQuery(q), user=user, deleted=False).order_by('-timeDate')
            pgx = ''
            template = loader.get_template('timesheet/timesheet_list_self.html')
            s = timeSum(timesheets_list)

    else:
        filterform = FilterForm(initial={'f':'Current_Month'})
        timesheets_dataset = timesheetDateFilter('Current_Month').filter(user=user)
        timesheets_dataset = timesheets_dataset.order_by('-timeDate').filter(user=user, deleted=False)
        s = timeSum(timesheets_dataset)
        timesheets_list = timesheets_dataset [a:b]
        length = timesheets_dataset.count()
        pgx = paginator(a, length, b)
        template = loader.get_template('timesheet/timesheet_list_self.html')

    context = {
        'timesheets_list': timesheets_list,
        'filterform' : filterform,
        's' : s,
        'pgx' : pgx,
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
@allowed_users(allowed_roles=['admin', 'staff', 'supervisor'])
def create_timesheet(request):
    if request.method == 'POST':
        timesheetform = TimesheetForm(request.POST)
        if timesheetform.is_valid():
            timesheetform.save()
            return HttpResponseRedirect('/timesheet/timesheets/0/10/')
        else:
            for error in timesheetform.errors.values():
                messages.error(request, error)

    else:
        timesheetform = TimesheetForm(initial={'timeItem': '8'})
        timesheetform.fields["project"].queryset = Project.objects.filter(projectStatus = True, deleted=False)

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
            time = timesheetform.save(commit=False)
            time.user = user
            time.save()
            return HttpResponseRedirect('/timesheet/timesheets_self/0/10/')
        else:
            for error in timesheetform.errors.values():
                messages.error(request, error)

    else:
        timesheetform = TimesheetForm(initial={'timeItem': '8'})
        timesheetform.fields["project"].queryset = Project.objects.filter(projectStatus = True, deleted=False)

    context = {
        'timesheetform': timesheetform,
        'title': _("Log Timesheet")
    }
    return render(request, 'timesheet/timesheet_create_self.html', context)


# Timesheet Update

@login_required
@allowed_users(allowed_roles=['admin', 'staff', 'supervisor'])
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
    
# Timesheet Delete Table (htmx)

@login_required
def delete_timesheet_table(request, id, u):
    uid = request.user.id
    timesheet = Time.objects.get(id=id)
    timesheet.deleted = 1
    timesheet.deletedBy = uid
    timesheet.save()
    return HttpResponse(status = 200)
    

# Timesheet Restore

@login_required
def restore_timesheet(request, id, u):
    timesheet = Time.objects.get(id=id)
    timesheet.deleted = 0
    timesheet.save()
    return HttpResponse(status = 200)

# Timesheet Full Delete

@login_required
def full_delete_timesheet(request, id):
    timesheet = Time.objects.get(id=id)
    timesheet.deletedBy = None
    timesheet.save()
    return HttpResponse(status = 200)

# Users List

@login_required
@allowed_users(allowed_roles=['admin', 'staff', 'supervisor'])
def users(request, a, b):
    if 'q' in request.GET or 'f' in request.GET:
        filterform = FilterForm(request.GET)
        if filterform.is_valid():   
            f = filterform.cleaned_data['f']
            q = filterform.cleaned_data['q']
            users_list = userAllocTime(f)
            if q:       
                users_list = users_list.annotate(search=SearchVector("last_name", "first_name")).filter(search=SearchQuery(q))
            pgx = ''
            template = loader.get_template('timesheet/user_list.html')
            total_alloc_time = users_list.aggregate(Sum('alloc_time'))
            total_unalloc_time = users_list.aggregate(Sum('unalloc_time'))
    else:
        users_dataset = userAllocTime('Current_Month')
        filterform = FilterForm(initial={'f':'Current_Month'})
        users_list =  users_dataset [a:b]
        total_alloc_time = users_dataset.aggregate(Sum('alloc_time'))
        total_unalloc_time = users_dataset.aggregate(Sum('unalloc_time'))
        length = users_dataset.count()
        pgx = paginator(a, length, b)
        template = loader.get_template('timesheet/user_list.html')
    
    context = {
        'users_list': users_list,
        'filterform' : filterform,
        'total_alloc_time' : total_alloc_time,
        'total_unalloc_time' : total_unalloc_time,
        'pgx' : pgx,
    }
    return HttpResponse(template.render(context, request))


# User Detail

@login_required
@allowed_users(allowed_roles=['admin', 'staff', 'supervisor'])
def user_detail(request, id, a, b):
    muser = get_user_model().objects.get(id=id)
    s = ''
    if muser.is_superuser == False:
        if 'q' in request.GET or 'f' in request.GET:
            filterform = FilterForm(request.GET)
            if filterform.is_valid():   
                f = filterform.cleaned_data['f']
                q = filterform.cleaned_data['q']
                project_list = getUserProjects(f, muser)
                if q:
                    project_list = project_list.annotate(search=SearchVector("projectName", "company__companyName")).filter(search=SearchQuery(q)).order_by('projectName')
                pgx = ''
                template = loader.get_template('timesheet/user_detail.html')
                s = project_list.aggregate(Sum('total_alloc_time'))
        
        else:
            filterform = FilterForm(initial={'f':'Current_Month'})
            project_dataset = getUserProjects('Current_Month', muser)
            s = project_dataset.aggregate(Sum('total_alloc_time'))
            project_list = project_dataset [a:b]
            length = project_dataset.count()
            pgx = paginator(a, length, b)
            template = loader.get_template('timesheet/user_detail.html')

        context = {
            'project_list': project_list,
            'filterform' : filterform,
            'id' : id,
            's' : s,
            'muser' : muser,
            'pgx' : pgx,
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/timesheet/users/0/10/')

##############
# htmx Views #
##############

# Timesheet Notes

@login_required
def timeNotes(request, id):
    '''Esta vista de la de display del partial de timesheet notes de htmx'''
    timesheet = Time.objects.get(id=id)
    context = {
        'timesheet' : timesheet,
    }
    return render(request, 'timesheet/partials/timesheet_notes.html', context)

@login_required
def timeNotesTitle(request, id):
    '''Esta vista de la de display del partial de timesheet notes de htmx'''
    timesheet = Time.objects.get(id=id)
    context = {
        'timesheet' : timesheet,
    }
    return render(request, 'timesheet/partials/timesheet_notes_title.html', context)

@login_required
def timeNotesEdit(request, id):
    '''Esta vista es el tramo de edición del partial de timesheet notes de htmx'''
    timesheet = Time.objects.get(id=id)
    if request.method == 'PUT':
        data = QueryDict(request.body).dict()
        notesform = TimeNotesForm(data, instance=timesheet)
        if notesform.is_valid():
            notesform.save()
            context = {
                'notesform' : notesform,
                'timesheet' : timesheet,
            }
            return render(request, 'timesheet/partials/timesheet_notes_title.html', context)

    else:
        notesform = TimeNotesForm(instance=timesheet)

    context = {
        'notesform' : notesform,
        'timesheet' : timesheet,
    }
    return render(request, 'timesheet/partials/timesheet_edit_notes.html', context)

# Company Notes:

@login_required
def companyNotes(request, id):
    '''Esta vista de la de display del partial de company notes de htmx'''
    company = Company.objects.get(id=id)
    context = {
        'company' : company,
    }
    return render(request, 'timesheet/partials/company_notes.html', context)

@login_required
def companyNotesTitle(request, id):
    '''Esta vista de la de display del partial de company notes de htmx'''
    company = Company.objects.get(id=id)
    context = {
        'company' : company,
    }
    return render(request, 'timesheet/partials/company_notes_title.html', context)

@login_required
def companyNotesEdit(request, id):
    '''Esta vista es el tramo de edición del partial de company notes de htmx'''
    company = Company.objects.get(id=id)
    if request.method == 'PUT':
        data = QueryDict(request.body).dict()
        notesform = CompanyNotesForm(data, instance=company)
        if notesform.is_valid():
            notesform.save()
            context = {
                'notesform' : notesform,
                'company' : company,
            }
            return render(request, 'timesheet/partials/company_notes_title.html', context)

    else:
        notesform = CompanyNotesForm(instance=company)

    context = {
        'notesform' : notesform,
        'company' : company,
    }
    return render(request, 'timesheet/partials/company_edit_notes.html', context)

# Project Notes:

@login_required
def projectNotes(request, id):
    '''Esta vista de la de display del partial de project notes de htmx'''
    project = Project.objects.get(id=id)
    context = {
        'project' : project,
    }
    return render(request, 'timesheet/partials/project_notes.html', context)

@login_required
def projectNotesTitle(request, id):
    '''Esta vista de la de display del partial de project notes de htmx'''
    project = Project.objects.get(id=id)
    context = {
        'project' : project,
    }
    return render(request, 'timesheet/partials/project_notes_title.html', context)

@login_required
def projectNotesEdit(request, id):
    '''Esta vista es el tramo de edición del partial de project notes de htmx'''
    project = Project.objects.get(id=id)
    if request.method == 'PUT':
        data = QueryDict(request.body).dict()
        notesform = ProjectNotesForm(data, instance=project)
        if notesform.is_valid():
            notesform.save()
            context = {
                'notesform' : notesform,
                'project' : project,
            }
            return render(request, 'timesheet/partials/project_notes_title.html', context)

    else:
        notesform = ProjectNotesForm(instance=project)

    context = {
        'notesform' : notesform,
        'project' : project,
    }
    return render(request, 'timesheet/partials/project_edit_notes.html', context)

# View Project (users w/sumarized time?)

# View Users (projects w/sumarized time?)

# def dev_button(request):
#     dateref = datetime.datetime(2023, 6, 15)
#     timesheets_list = Time.objects.order_by('-timeDate').filter(deleted=False, timeDate__lt=dateref)
#     timesheets_list=list(timesheets_list)
#     print(timesheets_list)
#     return redirect('/timesheet/timesheets/0/10/')