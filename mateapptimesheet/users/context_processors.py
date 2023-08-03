from django.conf import settings

def self_registration(request):
    return {'REGISTRATION_SELF_ENABLE': settings.REGISTRATION_SELF_ENABLE}