# Generated by Django 3.0.3 on 2020-06-19 11:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classform', '0002_auto_20200522_1255'),
        ('attendence', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentattendence',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendence', to='classform.ClassRoomStudent'),
        ),
    ]
