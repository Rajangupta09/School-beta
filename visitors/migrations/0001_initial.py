# Generated by Django 3.0.3 on 2020-05-16 14:24

from django.db import migrations, models
import visitors.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('mobile_no', models.BigIntegerField()),
                ('date_time', models.DateTimeField()),
                ('contact_to', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=50)),
                ('purpose', models.TextField(max_length=30)),
                ('photo', models.FileField(upload_to=visitors.models.user_directory_path)),
                ('document', models.FileField(upload_to=visitors.models.user_directory_path)),
            ],
        ),
    ]
