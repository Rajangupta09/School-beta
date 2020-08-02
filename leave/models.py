from django.db import models
from employeeform.models import Employee
from form.models import StudentInfo
status_op = (('Submitted','Submitted'),
               ('Approved','Approved'),
               ('Rejected','Rejected'),)
# Create your models here.

def employee_user_directory_path(instance, filename):
    """file will be uploaded to given path"""
    return 'employee/{0}/{1}'.format(instance.employee.empID, filename)


class EmployeeLeave(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
	description = models.TextField()
	subject = models.CharField(max_length=20)
	date_from = models.DateField()
	date_to = models.DateField()
	approved = models.BooleanField(default=False)
	rejected = models.BooleanField(default=False)
	status = models.CharField(max_length=100,null=True,blank=True,choices=status_op,default="Submitted")
	submit_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
	leave_file =  models.FileField(null=True, upload_to=employee_user_directory_path)


def user_directory_path(instance, filename):
    """file will be uploaded to given path"""
    return 'student/{0}/{1}/{2}'.format(instance.student.admissionNumber, filename,instance.id)




class StudentLeave(models.Model):
	student = models.ForeignKey(StudentInfo, on_delete=models.CASCADE)
	description = models.TextField()
	subject = models.CharField(max_length=20)
	date_from = models.DateField()
	date_to = models.DateField()
	approved = models.BooleanField(default=False)
	rejected = models.BooleanField(default=False)
	status = models.CharField(max_length=100,null=True,blank=True,choices=status_op,default="Submitted")
	submit_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
	leave_file =  models.FileField(null=True, upload_to=user_directory_path)
