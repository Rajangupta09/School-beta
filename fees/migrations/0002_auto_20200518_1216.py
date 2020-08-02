# Generated by Django 3.0.3 on 2020-05-18 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feecategory',
            name='description',
        ),
        migrations.RemoveField(
            model_name='feecategory',
            name='once',
        ),
        migrations.RemoveField(
            model_name='feecategory',
            name='submission_type',
        ),
        migrations.AddField(
            model_name='feecategory',
            name='deduction_order',
            field=models.IntegerField(default=0, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='feecategory',
            name='name',
            field=models.TextField(default=0, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='feecategory',
            name='submisstion_mode',
            field=models.CharField(choices=[('monthly', 'Monthly'), ('anually', 'Anually')], default='anually', max_length=30),
        ),
    ]