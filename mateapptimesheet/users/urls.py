from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name = 'Register'),
    path('profile/', views.profileView , name = 'profileView'),
    path('change_password/', views.passwordChange, name = 'passwordChange'),
    path('profile_edit/', views.profileEdit , name = 'profileEdit'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('password_reset/', views.passwordResetRequest, name = 'passwordReset'),
    path('password_reset_confirm/<uidb64>/<token>/', views.passwordResetConfirm, name='passwordResetConfirm'),
    path('users/<int:a>/<int:b>/', views.users, name = 'Users'),
    path('user/<int:id>/', views.user, name='User'),
    path('create_user/', views.create_user, name = 'createUser'),
    path('edit_user/<int:id>', views.edit_user, name = 'editUser'),
]