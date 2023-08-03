from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings

def user_not_authenticated(function=None, redirect_url='/'):
    """
    Decorator for views that checks that the user is NOT logged in, redirecting
    to the homepage if necessary by default.
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_url)
                
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    if function:
        return decorator(function)

    return decorator

def allowed_users(allowed_roles=[]):
    """
    Decorator for views that limits access for superuser or staff users.
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user:
                is_admin = request.user.is_superuser
                is_staff = request.user.is_staff
            if 'admin' in allowed_roles and is_admin:
                return view_func(request, *args, **kwargs)
            elif 'staff' in allowed_roles and is_staff:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'You are not allowed to access that page.')
                return redirect('/')
        return _wrapped_view
    return decorator

def self_registration_enabled(function=None, redirect_url='/'):
    """
    Decorator to check if self registration is enabled.
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not settings.REGISTRATION_SELF_ENABLE:
                messages.error(request, 'You are not allowed to access that page.')
                return redirect(redirect_url)
                
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    if function:
        return decorator(function)

    return decorator