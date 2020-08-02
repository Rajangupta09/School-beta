# Generated by Django 3.0.3 on 2020-05-26 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0001_initial'),
        ('fees', '0039_auto_20200526_1416'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentdiscount',
            name='classroom_students',
        ),
        migrations.AddField(
            model_name='studentdiscount',
            name='student',
            field=models.ManyToManyField(related_name='fee_discounts', to='form.StudentInfo'),
        ),
        migrations.AlterField(
            model_name='feediscount',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fees.Session'),
        ),
    ]
