#### ONLY LINUX

from django.core.management import call_command

def backup():
    try:
        call_command('dbbackup', clean=True, interactive=False)
    except:
        pass