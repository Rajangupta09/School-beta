# Generated by Django 3.0.3 on 2020-06-08 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('classform', '0002_auto_20200522_1255'),
        ('timetable', '0001_initial'),
        ('fees', '0043_studentdiscount_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('examName', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ExamMapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minMarks', models.IntegerField(blank=True, default=None, null=True)),
                ('maxMarks', models.IntegerField(blank=True, default=100)),
                ('weightage', models.IntegerField(blank=True, default=None, null=True)),
                ('classsubject', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='timetable.ClassRoomSubjectTeacher')),
            ],
        ),
        migrations.CreateModel(
            name='Marks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks', models.IntegerField(blank=True, default=None, null=True)),
                ('grade', models.CharField(blank=True, max_length=5, null=True)),
                ('maxusermarks', models.IntegerField(blank=True, default=0, null=True)),
                ('weightage', models.IntegerField(blank=True, default=None, null=True)),
                ('remarks', models.CharField(blank=True, max_length=50, null=True)),
                ('classroomStudent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classform.ClassRoomStudent')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='markssection.ExamMapping')),
            ],
        ),
        migrations.CreateModel(
            name='ExamType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('examType', models.CharField(blank=True, max_length=50, null=True)),
                ('maxMarks', models.IntegerField(blank=True, null=True)),
                ('priority', models.IntegerField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('classroom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='classform.ClassRoom')),
                ('examName', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='markssection.Exam')),
                ('session', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fees.Session')),
            ],
        ),
        migrations.AddField(
            model_name='exammapping',
            name='examType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='markssection.ExamType'),
        ),
        migrations.AddField(
            model_name='exammapping',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fees.Session'),
        ),
        migrations.CreateModel(
            name='AdditionalSubjectMapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=50)),
                ('marks', models.IntegerField(blank=True, null=True)),
                ('classroomStudent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classform.ClassRoomStudent')),
                ('examName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='markssection.Exam')),
                ('examType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='markssection.ExamType')),
            ],
        ),
    ]
