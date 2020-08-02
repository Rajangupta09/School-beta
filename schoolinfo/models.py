from django.db import models

# Create your models here.


def user_directory_path(instance, filename):
    """file will be uploaded to given path"""
    return 'schoolInfo/{0}/{1}'.format(instance.schoolName, filename)


class SchoolInfo(models.Model):
    schoolName = models.CharField(max_length=100)
    addresss = models.CharField(max_length=100, blank=True, null=True)
    principalName = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zipCode = models.IntegerField(blank=True, null=True)
    schoolID = models.IntegerField(primary_key=True)
    longitude = models.IntegerField(blank=True, null=True)
    latitude = models.IntegerField(blank=True, null=True)
    contactNumber = models.IntegerField(blank=True, null=True)
    webSiteURL = models.CharField(max_length=100, blank=True, null=True)
    img = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    logo = models.FileField(upload_to=user_directory_path, blank=True, null=True)

