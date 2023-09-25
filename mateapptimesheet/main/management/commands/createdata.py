import random
import calendar
from datetime import date
from django.core.management.base import BaseCommand
from faker import Faker
from timesheet.models import Project, Company, Time
from django.contrib.auth import get_user_model

# users = get_user_model().objects.get(all)

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        
        users = get_user_model().objects.filter(is_active=True).exclude(is_superuser=True).order_by('id')
        uids = []
        for user in users:
            uids.append(user.id)
        print(uids)

        c = calendar.Calendar()
        for date in c.itermonthdates(2023, 8):
            print(date)