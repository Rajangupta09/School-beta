# Generated by Django 3.0.3 on 2020-05-18 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0011_auto_20200518_1909'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feecycle',
            name='last_submission_date',
        ),
    ]
