# Generated by Django 3.0.3 on 2020-05-23 08:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0001_initial'),
        ('fees', '0031_feeheadmapping'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feeheadmapping',
            name='classroom_student',
        ),
        migrations.AddField(
            model_name='feeheadmapping',
            name='student',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='form.StudentInfo'),
            preserve_default=False,
        ),
    ]