"""
Tables for student form
"""
from django.db import models
from transport.models import RouteDetail
from django.core.exceptions import ValidationError
from PIL import Image
# Create your models here.


class StudentInfo(models.Model):
    """Student Table"""
    firstName = models.CharField(max_length=20, blank=True)
    lastName = models.CharField(max_length=20, blank=True)
    fullName = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    dob = models.DateField(null=True, blank=True)
    classSection = models.CharField(max_length=20, blank=True)
    admissionNumber = models.BigIntegerField(primary_key=True)
    mobileNumber = models.BigIntegerField(null=True, blank=True)
    religion = models.CharField(max_length=20, blank=True)
    caste = models.CharField(max_length=20, blank=True)
    tcNumber = models.BigIntegerField(null=True, blank=True)
    aadharNumber = models.BigIntegerField(null=True, blank=True)
    feeWaiverCategory = models.CharField(max_length=20, blank=True)
    siblingID = models.BigIntegerField(null=True, blank=True)
    siblingID0 = models.BigIntegerField(null=True, blank=True)
    siblingID1 = models.BigIntegerField(null=True, blank=True)
    siblingID2 = models.BigIntegerField(null=True, blank=True)
    prevschoolname = models.CharField(blank=True, null=True, max_length=100)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.admissionNumber}"


class CurrentAddress(models.Model):
    """Currrent Address Table"""
    student = models.OneToOneField(
        StudentInfo, primary_key=True, on_delete=models.CASCADE, related_name='address')
    Address = models.CharField(max_length=100, blank=True)
    Address1 = models.CharField(max_length=100, blank=True)
    Address2 = models.CharField(max_length=100, blank=True)
    zipCode = models.BigIntegerField(null=True, blank=True)
    state = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Name:{self.student.fullName}"


class PermanentAddress(models.Model):
    """Permanent Address Table"""
    student = models.OneToOneField(
        StudentInfo, primary_key=True, on_delete=models.CASCADE)
    Address = models.CharField(max_length=100, blank=True)
    Address1 = models.CharField(max_length=100, blank=True)
    Address2 = models.CharField(max_length=100, blank=True)
    zipCode = models.BigIntegerField(null=True, blank=True)
    state = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Name:{self.student.fullName}"


class ParentInfo(models.Model):
    """ Parents Info Table"""
    student = models.OneToOneField(
        StudentInfo, primary_key=True, on_delete=models.CASCADE, related_name='parent')
    fatherName = models.CharField(max_length=20, blank=True)
    motherName = models.CharField(max_length=20, blank=True)
    Fatherdob = models.DateField(null=True, blank=True)
    Motherdob = models.DateField(null=True, blank=True)
    MobileNumber = models.BigIntegerField(null=True, blank=True)
    altMobileNumber = models.BigIntegerField(null=True, blank=True)
    gaurdianQual = models.CharField(max_length=30, blank=True, null=True)
    guardianOccup = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True)
    motherQual = models.CharField(max_length=30, blank=True, null=True)
    motherOccup = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Student:{self.student.fullName} Add.No: {self.student.admissionNumber} Father Name:{self.fatherName}"


def user_directory_path(instance, filename):
    """file will be uploaded to given path"""
    return 'student/{0}/{1}'.format(instance.student.admissionNumber, filename)


class Documents(models.Model):
    """Document Table"""
    student = models.OneToOneField(
        StudentInfo, primary_key=True, on_delete=models.CASCADE)
    photo = models.FileField(null=True, upload_to=user_directory_path)
    idProof = models.FileField(null=True, upload_to=user_directory_path)
    castCertificate = models.FileField(
        null=True, upload_to=user_directory_path)
    domicile = models.FileField(null=True, upload_to=user_directory_path)
    tc = models.FileField(null=True, upload_to=user_directory_path)
    characterCertificate = models.FileField(
        null=True, upload_to=user_directory_path)

    def __str__(self):
        return f"Name:{self.student.fullName}"

    def save(self, *args, **kwargs):
        super(Documents, self).save(*args, **kwargs)

        # compress only if IMG file
        try:
            img = Image.open(self.image.path)  # Open image using self

            if img.height > 400 or img.width > 400:
                new_img = (400, 400)
                img.thumbnail(new_img)
                img.save(self.image.path)

        # else ingore
        except:
            pass


class StudentRoute(models.Model):
    student = models.ForeignKey(StudentInfo, on_delete=models.CASCADE)
    stoppage = models.CharField(max_length=30, null=True, blank=True)
    shift = models.ForeignKey(RouteDetail, null=True,
                              on_delete=models.PROTECT, related_name='students')

    class Meta:
        unique_together = (('student', 'shift'),)
