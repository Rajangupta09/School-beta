# Generated by Django 3.0.3 on 2020-05-18 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0002_auto_20200518_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feecategory',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
