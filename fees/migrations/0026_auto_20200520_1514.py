# Generated by Django 3.0.3 on 2020-05-20 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0025_auto_20200520_1513'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feediscount',
            name='percentage',
        ),
        migrations.RemoveField(
            model_name='feediscount',
            name='total_off',
        ),
    ]