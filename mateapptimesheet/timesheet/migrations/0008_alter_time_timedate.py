# Generated by Django 4.2.2 on 2023-06-12 13:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheet', '0007_remove_time_timeduration_time_timedate_time_timeitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='time',
            name='timeDate',
            field=models.DateField(default=datetime.date.today, null=True),
        ),
    ]
