# Generated by Django 3.0.6 on 2020-05-21 16:48

from django.db import migrations, models
import schoolinfo.models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolinfo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolinfo',
            name='addresss',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='schoolinfo',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='schoolinfo',
            name='contactNumber',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='schoolinfo',
            name='email',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='schoolinfo',
            name='img',
            field=models.FileField(blank=True, null=True, upload_to=schoolinfo.models.user_directory_path),
        ),
        migrations.AlterField(
            model_name='schoolinfo',
            name='latitude',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='schoolinfo',
            name='logo',
            field=models.FileField(blank=True, null=True, upload_to=schoolinfo.models.user_directory_path),
        ),
        migrations.AlterField(
            model_name='schoolinfo',
            name='longitude',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='schoolinfo',
            name='principalName',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='schoolinfo',
            name='state',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='schoolinfo',
            name='webSiteURL',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='schoolinfo',
            name='zipCode',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]