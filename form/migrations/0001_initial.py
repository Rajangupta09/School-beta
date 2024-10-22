# Generated by Django 3.0.3 on 2020-05-16 14:24

from django.db import migrations, models
import django.db.models.deletion
import form.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('transport', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentInfo',
            fields=[
                ('firstName', models.CharField(blank=True, max_length=20)),
                ('lastName', models.CharField(blank=True, max_length=20)),
                ('fullName', models.CharField(blank=True, max_length=50)),
                ('gender', models.CharField(blank=True, max_length=20)),
                ('dob', models.DateField(blank=True, null=True)),
                ('classSection', models.CharField(blank=True, max_length=20)),
                ('admissionNumber', models.BigIntegerField(primary_key=True, serialize=False)),
                ('mobileNumber', models.BigIntegerField(blank=True, null=True)),
                ('religion', models.CharField(blank=True, max_length=20)),
                ('caste', models.CharField(blank=True, max_length=20)),
                ('tcNumber', models.BigIntegerField(blank=True, null=True)),
                ('aadharNumber', models.BigIntegerField(blank=True, null=True)),
                ('feeWaiverCategory', models.CharField(blank=True, max_length=20)),
                ('siblingID', models.BigIntegerField(blank=True, null=True)),
                ('siblingID0', models.BigIntegerField(blank=True, null=True)),
                ('siblingID1', models.BigIntegerField(blank=True, null=True)),
                ('siblingID2', models.BigIntegerField(blank=True, null=True)),
                ('prevschoolname', models.CharField(blank=True, max_length=100, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CurrentAddress',
            fields=[
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='form.StudentInfo')),
                ('Address', models.CharField(blank=True, max_length=100)),
                ('Address1', models.CharField(blank=True, max_length=100)),
                ('Address2', models.CharField(blank=True, max_length=100)),
                ('zipCode', models.BigIntegerField(blank=True, null=True)),
                ('state', models.CharField(blank=True, max_length=20)),
                ('city', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='form.StudentInfo')),
                ('photo', models.FileField(null=True, upload_to=form.models.user_directory_path)),
                ('idProof', models.FileField(null=True, upload_to=form.models.user_directory_path)),
                ('castCertificate', models.FileField(null=True, upload_to=form.models.user_directory_path)),
                ('domicile', models.FileField(null=True, upload_to=form.models.user_directory_path)),
                ('tc', models.FileField(null=True, upload_to=form.models.user_directory_path)),
                ('characterCertificate', models.FileField(null=True, upload_to=form.models.user_directory_path)),
            ],
        ),
        migrations.CreateModel(
            name='ParentInfo',
            fields=[
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='parent', serialize=False, to='form.StudentInfo')),
                ('fatherName', models.CharField(blank=True, max_length=20)),
                ('motherName', models.CharField(blank=True, max_length=20)),
                ('Fatherdob', models.DateField(blank=True, null=True)),
                ('Motherdob', models.DateField(blank=True, null=True)),
                ('MobileNumber', models.BigIntegerField(blank=True, null=True)),
                ('altMobileNumber', models.BigIntegerField(blank=True, null=True)),
                ('gaurdianQual', models.CharField(blank=True, max_length=30, null=True)),
                ('guardianOccup', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('motherQual', models.CharField(blank=True, max_length=30, null=True)),
                ('motherOccup', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PermanentAddress',
            fields=[
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='form.StudentInfo')),
                ('Address', models.CharField(blank=True, max_length=100)),
                ('Address1', models.CharField(blank=True, max_length=100)),
                ('Address2', models.CharField(blank=True, max_length=100)),
                ('zipCode', models.BigIntegerField(blank=True, null=True)),
                ('state', models.CharField(blank=True, max_length=20)),
                ('city', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='StudentRoute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stoppage', models.CharField(blank=True, max_length=30, null=True)),
                ('shift', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='students', to='transport.RouteDetail')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='form.StudentInfo')),
            ],
            options={
                'unique_together': {('student', 'shift')},
            },
        ),
    ]
