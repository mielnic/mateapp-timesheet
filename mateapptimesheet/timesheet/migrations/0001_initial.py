# Generated by Django 4.2.2 on 2023-06-07 19:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(blank=True, max_length=200)),
                ('postalCode', models.CharField(blank=True, max_length=7)),
                ('city', models.CharField(blank=True, max_length=50)),
                ('state', models.CharField(blank=True, max_length=50)),
                ('country', models.CharField(blank=True, max_length=50)),
                ('deleted', models.BooleanField(blank=True, default=0)),
                ('deletedBy', models.BigIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyName', models.CharField(blank=True, max_length=100)),
                ('tax_id', models.CharField(blank=True, max_length=15)),
                ('website', models.CharField(blank=True, max_length=100)),
                ('companyPhone', models.CharField(blank=True, max_length=25)),
                ('companyNotes', models.CharField(blank=True, max_length=500)),
                ('deleted', models.BooleanField(blank=True, default=0)),
                ('deletedBy', models.BigIntegerField(blank=True, null=True)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='timesheet.address')),
            ],
        ),
        migrations.CreateModel(
            name='Contractor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contractorName', models.CharField(blank=True, max_length=100)),
                ('deleted', models.BooleanField(blank=True, default=0)),
                ('deletedBy', models.BigIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeDuration', models.DurationField()),
                ('timeType', models.CharField(blank=True, max_length=100)),
                ('user', models.BigIntegerField(blank=True, null=True)),
                ('timeNotes', models.CharField(blank=True, max_length=500)),
                ('deleted', models.BooleanField(blank=True, default=0)),
                ('deletedBy', models.BigIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projectName', models.CharField(blank=True, max_length=100)),
                ('deleted', models.BooleanField(blank=True, default=0)),
                ('deletedBy', models.BigIntegerField(blank=True, null=True)),
                ('contractor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='timesheet.contractor')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='timesheet.company')),
            ],
        ),
    ]
