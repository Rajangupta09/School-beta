# Generated by Django 3.0.3 on 2020-06-13 06:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0001_initial'),
        ('fees', '0048_auto_20200612_1114'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeeStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.PositiveIntegerField()),
                ('total_amount', models.PositiveIntegerField()),
                ('received', models.PositiveIntegerField()),
                ('balance', models.PositiveIntegerField()),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fees.Session')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='form.StudentInfo')),
            ],
            options={
                'unique_together': {('student', 'session')},
            },
        ),
    ]
