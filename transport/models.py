from django.db import models
from employeeform.models import Employee
# Create your models here.


class Vehicle(models.Model):
    vehicle_no = models.BigIntegerField(primary_key=True)
    device_id = models.BigIntegerField()
    service_id = models.BigIntegerField()
    no_of_seat = models.IntegerField()
    maximum_allowed = models.IntegerField()
    vehicle_type = models.CharField(max_length=30, default="")
    insurance_company = models.CharField(max_length=30, default="")
    contact_person = models.CharField(max_length=30, default="", blank=True)
    insurance_date = models.DateField(null=True, blank=True)
    permit_valid_date = models.DateField(null=True, blank=True)
    pollution_cert_exp_date = models.DateField(null=True, blank=True)
    service_date = models.DateField(null=True, blank=True)
    fitness_service_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.vehicle_no)


def user_directory_path(instance, filename):
    """file will be uploaded to given path"""
    return 'emp/{0}/{1}'.format(instance.employee.empID, filename)


class Driver(models.Model):
    employee = models.OneToOneField(
        Employee, primary_key=True, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    license_no = models.BigIntegerField()
    batch_no = models.BigIntegerField()
    driverPic = models.FileField(
        upload_to=user_directory_path, null=True, verbose_name='Driver Picture')
    driverLicense = models.FileField(
        upload_to=user_directory_path, verbose_name='Driver License')
    driverID = models.FileField(
        upload_to=user_directory_path, null=True, verbose_name='Driver Name')


class Routes(models.Model):

    class Shift(models.TextChoices):
        AFTERNOON = 'afternoon'
        MORNING = 'morning',
        BOTH = 'both'

    """
    auto generated field and route_id were causing issues
    thus use this routeID. this auto field creates an issue in postgresql 
    databse mentioned in save() method below
    """
    routeID = models.AutoField(primary_key=True)
    route_code = models.CharField(unique=True, max_length=110, blank=False)
    archived = models.BooleanField(null=True, blank=True)
    shift_time = models.CharField(
        max_length=30,
        choices=Shift.choices,
        default=Shift.MORNING,
        null=False,
        blank=False
    )

    def save(self, *args, **kwargs):
        """
            Django is not populating autofield for some reason(in postgres sql)
            so we have to do it manually
        """
        if not self.routeID:
            self.routeID = Routes.objects.last().routeID + 1 if Routes.objects.last() else 1
        return super().save(*args, **kwargs)


class RouteVehicle(models.Model):
    route = models.ForeignKey(
        Routes, related_name='vehicles', on_delete=models.CASCADE)
    vehicle = models.ForeignKey(
        Vehicle, related_name='routes', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('route', 'vehicle'),)


class RouteDetail(models.Model):

    # route_code_1 for morning route
    # route_code_2 for afternoon route
    route_code_1 = models.OneToOneField(
        Routes,
        null=True,
        related_name='morning_shift',
        on_delete=models.CASCADE
    )
    route_code_2 = models.OneToOneField(
        Routes,
        null=True,
        related_name='afternoon_shift',
        on_delete=models.CASCADE
    )
    sub_route_code = models.CharField(unique=True, max_length=110, blank=False)
    remarks = models.CharField(max_length=50, null=True)
    route_distance = models.IntegerField(null=True,)
    start_place = models.CharField(max_length=30, null=False, blank=False)
    end_place = models.CharField(max_length=30, null=False, blank=False)
    archived = models.BooleanField(null=True, blank=True)
    start_lattitude = models.DecimalField(
        max_digits=8,
        decimal_places=4,
        null=False,
        blank=False
    )
    start_longitude = models.DecimalField(
        max_digits=8,
        decimal_places=4,
        null=False,
        blank=False
    )
    end_lattitude = models.DecimalField(
        max_digits=8,
        decimal_places=4,
        null=False,
        blank=False
    )
    end_longitude = models.DecimalField(
        max_digits=8,
        decimal_places=4,
        null=False,
        blank=False
    )


class Stoppage(models.Model):
    route_detail = models.ForeignKey(
        RouteDetail, on_delete=models.CASCADE, related_name='stoppagess')
    stoppage_name = models.CharField(max_length=100, null=False, blank=False)
    longitude = models.DecimalField(
        max_digits=8,
        decimal_places=4,
        null=False,
        blank=False
    )
    lattitude = models.DecimalField(
        max_digits=8,
        decimal_places=4,
        null=False,
        blank=False
    )
