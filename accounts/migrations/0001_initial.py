# Generated by Django 3.0.3 on 2020-05-16 14:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullName', models.CharField(default='', max_length=50)),
                ('user_type', models.CharField(default='', max_length=20)),
                ('mobile_no', models.BigIntegerField(default=0)),
                ('image', models.ImageField(default='default.jpg', upload_to='profile_pics')),
                ('emp_id', models.BigIntegerField(default=0)),
                ('addmission_number', models.BigIntegerField(default=0)),
                ('password', models.CharField(default='', max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
