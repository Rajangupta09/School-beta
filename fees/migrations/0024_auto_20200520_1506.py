# Generated by Django 3.0.3 on 2020-05-20 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0023_feediscount_session'),
    ]

    operations = [
        migrations.AddField(
            model_name='feediscount',
            name='discount',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='feediscount',
            name='discount_type',
            field=models.CharField(choices=[('percentage', 'Percentage'), ('absolute', 'Absolute')], default='percentage', max_length=30),
        ),
    ]
