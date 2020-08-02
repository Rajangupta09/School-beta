# Generated by Django 3.0.3 on 2020-05-16 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employeeform', '0001_initial'),
        ('form', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentLeave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('subject', models.CharField(max_length=20)),
                ('date_from', models.DateField()),
                ('date_to', models.DateField()),
                ('approved', models.BooleanField(default=False)),
                ('rejected', models.BooleanField(default=False)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='form.StudentInfo')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeLeave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('subject', models.CharField(max_length=20)),
                ('date_from', models.DateField()),
                ('date_to', models.DateField()),
                ('approved', models.BooleanField(default=False)),
                ('rejected', models.BooleanField(default=False)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employeeform.Employee')),
            ],
        ),
    ]
