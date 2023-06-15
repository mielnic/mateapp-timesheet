from django.urls import path, include
from . import views
from timesheet.views import create_self_timesheet

app_name = 'main'

urlpatterns = [
    path('', create_self_timesheet, name = 'Create_Self_Timesheet'),
    path('login/', views.login, name='login'),
    path('signout/', views.signout, name='Logout'),
    path('user_trash/<int:a>/<int:b>/', views.user_trash, name='User_Trash'),
    path('admin_trash/<int:a>/<int:b>/', views.admin_trash, name='Admin_Trash'),
    path('admin_home/<int:a>/<int:b>/', views.admin_home, name='Admin_Home'),
    path('search/', views.search, name='Search')
    # path('backup/', views.do_backup, name='Backup'),
]
