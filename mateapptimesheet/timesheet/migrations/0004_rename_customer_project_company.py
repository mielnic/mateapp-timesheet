# Generated by Django 4.2.2 on 2023-06-08 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheet', '0003_alter_project_contractor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='customer',
            new_name='company',
        ),
    ]
