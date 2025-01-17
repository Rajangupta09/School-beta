# Generated by Django 3.0.3 on 2020-05-21 03:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classform', '0001_initial'),
        ('fees', '0028_auto_20200520_1607'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentDiscount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classroom_student', models.ManyToManyField(related_name='discounts', to='classform.ClassRoomStudent')),
                ('discount_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fees.FeeDiscount')),
            ],
        ),
    ]
