# Generated by Django 3.0.3 on 2020-05-16 14:24

from django.db import migrations, models
import gallery.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('album_name', models.CharField(max_length=30)),
                ('file', models.FileField(upload_to=gallery.models.album_directory_path)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo_name', models.CharField(max_length=30)),
                ('file', models.FileField(upload_to=gallery.models.photo_directory_path)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_name', models.CharField(max_length=30)),
                ('file', models.FileField(upload_to=gallery.models.video_directory_path)),
            ],
        ),
    ]
