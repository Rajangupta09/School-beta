# Generated by Django 3.0.3 on 2020-05-22 07:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classform', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroomstudent',
            name='classRoom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='classform.ClassRoom'),
        ),
    ]