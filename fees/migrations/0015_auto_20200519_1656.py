# Generated by Django 3.0.3 on 2020-05-19 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0014_classfeeconfiguration_feeconfiguration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classfeeconfiguration',
            name='amount',
        ),
        migrations.AddField(
            model_name='feeconfiguration',
            name='amount',
            field=models.FloatField(default=120),
            preserve_default=False,
        ),
    ]