from django.urls import path, include, reverse
from . import views

app_name = 'timesheet'

# Customers

urlpatterns = [
    path('create_company/', views.create_company, name='Create_Company'),
    path('edit_company/<int:id>/', views.edit_company, name='Edit_Company'),
    path('delete_company/<int:id>/', views.delete_company, name='Delete_Company'),
    path('restore_company/<int:id>/<int:u>/', views.restore_company, name='Restore_Company'),
    path('full_delete_company/<int:id>/', views.full_delete_company, name='Full_Delete_Company'),
    path('companies/<int:a>/<int:b>/', views.companies , name='Companies'),
    path('company/<int:id>/<int:a>/<int:b>/', views.company , name='Company'),
]

# Projects

urlpatterns += [
    path('create_project/', views.create_project, name='Create_Project'),
    path('edit_project/<int:id>/', views.edit_project, name='Edit_Project'),
    path('delete_project/<int:id>/', views.delete_project, name='Delete_Project'),
    path('restore_project/<int:id>/<int:u>/', views.restore_project, name='Restore_Project'),
    path('full_delete_project/<int:id>/', views.full_delete_project, name='Full_Delete_Project'),
    path('projects/<int:a>/<int:b>/', views.projects , name='Projects'),
    path('project/<int:id>/<int:a>/<int:b>/', views.project , name='Project'),
]

# Timesheet

urlpatterns += [
    path('create_timesheet/', views.create_timesheet, name='Create_Timesheet'),
    path('create_self_timesheet/', views.create_self_timesheet, name='Create_Self_Timesheet'),
    path('edit_timesheet/<int:id>/', views.edit_timesheet, name='Edit_Timesheet'),
    path('edit_self_timesheet/<int:id>/', views.edit_self_timesheet, name='Edit_Self_Timesheet'),
    path('delete_timesheet_table/<int:id>/<int:u>/', views.delete_timesheet_table, name='Delete_Timesheet_Table'),
    path('delete_timesheet/<int:id>/<int:u>/', views.delete_timesheet, name='Delete_Timesheet'),
    path('restore_timesheet/<int:id>/<int:u>/', views.restore_timesheet, name='Restore_Timesheet'),
    path('full_delete_timesheet/<int:id>/', views.full_delete_timesheet, name='Full_Delete_Timesheet'),
    path('timesheets/<int:a>/<int:b>/', views.timesheets , name='Timesheets'),
    path('timesheets_self/<int:a>/<int:b>/', views.self_timesheets , name='Self_Timesheets'),
    path('timesheet/<int:id>/', views.timesheet , name='Timesheet'),
    path('timesheet_self/<int:id>/', views.timesheet_self , name='Timesheet_Self'),
]

# Users

urlpatterns += [
    path('users/<int:a>/<int:b>/', views.users, name='Users'),
    path('user/<int:id>/<int:a>/<int:b>/', views.user_detail, name='User'),
]


# urlpatterns += [
#     path('dev', views.dev_button, name='Dev'),
# ]