# Generated by Django 3.0.3 on 2020-05-16 14:24

from django.db import migrations, models
import django.db.models.deletion
import homework.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('classform', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Syllabus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('document', models.FileField(blank=True, upload_to=homework.models.user_syllabus_path)),
                ('date_published', models.DateField()),
                ('classRoom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classform.ClassRoom')),
            ],
        ),
        migrations.CreateModel(
            name='HomeWork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('subject', models.CharField(max_length=100)),
                ('document', models.FileField(blank=True, upload_to=homework.models.user_directory_path)),
                ('date_published', models.DateField()),
                ('classRoom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classform.ClassRoom')),
            ],
        ),
    ]