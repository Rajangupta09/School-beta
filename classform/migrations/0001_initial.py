# Generated by Django 3.0.3 on 2020-05-16 14:24

import classform.models
import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('form', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classSection', models.CharField(max_length=50)),
                ('_class', models.CharField(blank=True, max_length=50)),
                ('_section', models.CharField(blank=True, max_length=50)),
                ('class_teacher_alloted', models.BooleanField(default=False)),
                ('room_no', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ClassRoomStudent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll_number', models.IntegerField()),
                ('classRoom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classform.ClassRoom')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='classroom_student', to='form.StudentInfo')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReportCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reportCard', models.FileField(upload_to=classform.models.user_directory_path)),
                ('class_room_student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classform.ClassRoomStudent')),
            ],
        ),
        migrations.CreateModel(
            name='StudentRouteAttendence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('time', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('student_route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='form.StudentRoute')),
            ],
            options={
                'unique_together': {('date', 'student_route')},
            },
        ),
    ]
