# Generated by Django 3.0.3 on 2020-06-12 05:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0047_auto_20200612_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feecycle',
            name='session',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='fees.Session'),
        ),
    ]
