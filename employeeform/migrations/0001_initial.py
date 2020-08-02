# Generated by Django 3.0.3 on 2020-05-16 14:24

from django.db import migrations, models
import django.db.models.deletion
import employeeform.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('empID', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('firstName', models.CharField(blank=True, max_length=20, verbose_name='First Name')),
                ('lastName', models.CharField(blank=True, max_length=20, verbose_name='Last Name')),
                ('fullName', models.CharField(blank=True, max_length=50, verbose_name='Full Name')),
                ('father_name', models.CharField(blank=True, max_length=50)),
                ('mother_name', models.CharField(blank=True, max_length=50)),
                ('partnerName', models.CharField(blank=True, max_length=50, verbose_name='Partner Name')),
                ('gender', models.CharField(blank=True, max_length=20)),
                ('email', models.CharField(blank=True, max_length=40)),
                ('currentAddress', models.CharField(blank=True, max_length=100, verbose_name='Current Address')),
                ('permanentAddress', models.CharField(blank=True, max_length=100, verbose_name='Permanent Address')),
                ('dob', models.DateField(blank=True, null=True)),
                ('joiningDate', models.DateField(blank=True, null=True, verbose_name='Joining Date')),
                ('bloodGroup', models.CharField(blank=True, max_length=20)),
                ('mobile_number', models.BigIntegerField(default=0)),
                ('marital_status', models.CharField(blank=True, max_length=20)),
                ('experience', models.CharField(blank=True, max_length=20)),
                ('aadharNumber', models.BigIntegerField(default=0, verbose_name='Aadhar Number')),
                ('empCategory', models.CharField(blank=True, max_length=20, verbose_name='Employee Category')),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CurrentAddress',
            fields=[
                ('employee', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='employeeform.Employee')),
                ('Address', models.CharField(blank=True, max_length=100)),
                ('Address1', models.CharField(blank=True, max_length=100)),
                ('Address2', models.CharField(blank=True, max_length=100)),
                ('zipCode', models.BigIntegerField(default=0)),
                ('state', models.CharField(blank=True, max_length=20)),
                ('city', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeDocuments',
            fields=[
                ('employee', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='employeeform.Employee')),
                ('photo', models.FileField(blank=True, upload_to=employeeform.models.user_directory_path)),
                ('qualificationDoc', models.FileField(blank=True, upload_to=employeeform.models.user_directory_path)),
                ('IdProof', models.FileField(blank=True, upload_to=employeeform.models.user_directory_path)),
                ('addressProof', models.FileField(blank=True, upload_to=employeeform.models.user_directory_path)),
                ('otherDoc', models.FileField(blank=True, upload_to=employeeform.models.user_directory_path)),
            ],
        ),
        migrations.CreateModel(
            name='PermanentAddress',
            fields=[
                ('employee', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='employeeform.Employee')),
                ('Address', models.CharField(blank=True, max_length=100)),
                ('Address1', models.CharField(blank=True, max_length=100)),
                ('Address2', models.CharField(blank=True, max_length=100)),
                ('zipCode', models.BigIntegerField(default=0)),
                ('state', models.CharField(blank=True, max_length=20)),
                ('city', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('employee', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='employeeform.Employee')),
                ('specialization', models.CharField(blank=True, max_length=50)),
                ('designation', models.CharField(blank=True, max_length=50)),
                ('classTeacher', models.CharField(blank=True, max_length=50)),
            ],
        ),
    ]