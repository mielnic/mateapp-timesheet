# Generated by Django 4.2.2 on 2023-06-09 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheet', '0006_remove_project_contractor_alter_time_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='time',
            name='timeDuration',
        ),
        migrations.AddField(
            model_name='time',
            name='timeDate',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='time',
            name='timeItem',
            field=models.IntegerField(null=True),
        ),
    ]
