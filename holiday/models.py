from django.db import models
from classform.models import ClassRoom

# Create your models here.


class Holidays(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    holiday_date = models.DateField()
    holiday_date_to = models.DateField(default=holiday_date)
    employeeholiday = models.CharField(max_length=200, null=True, blank=True)
    classroom = models.ForeignKey(
        ClassRoom,
        null=True,
        on_delete=models.CASCADE,
        related_name='holidays_class'
    )
    category = models.CharField(max_length=200)

    def __str__(self):
        return f"Date:{self.holiday_date}"
