# Generated by Django 3.0.3 on 2020-06-17 18:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currentaddress',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='address', serialize=False, to='form.StudentInfo'),
        ),
    ]
