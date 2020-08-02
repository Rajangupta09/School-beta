"""
Database tables for attendence app
"""

from django.db import models
from form.models import StudentInfo
from classform.models import ClassRoomStudent
from employeeform.models import Employee

# Create your models here.


class StudentAttendence(models.Model):
    """
    Student Attendence table
    """
    student = models.ForeignKey(ClassRoomStudent, on_delete=models.CASCADE, related_name='attendence')
    status = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField(auto_now=True)
    available_casual_leave = models.IntegerField(default=10)
    available_sick_leave = models.IntegerField(default=10)
    taken_casual_leave = models.IntegerField(default=0)
    taken_sick_leave = models.IntegerField(default=0)
    total_no_of_days_present = models.IntegerField(default=0)
    total_no_of_days_late = models.IntegerField(default=0)
    def __str__(self):
        return f"Name:{self.student.student.fullName}| Date:{self.date} | Status:{self.status} | Class: {self.student.classRoom.classSection} | Admission No:{self.student.student.admissionNumber} | ({self.time})"


class TeacherAttendence(models.Model):
    """
    Teacher Attendence Table
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField(auto_now=True)
    available_casual_leave = models.IntegerField(default=10)
    available_sick_leave = models.IntegerField(default=10)
    taken_casual_leave = models.IntegerField(default=0)
    taken_sick_leave = models.IntegerField(default=0)
    total_no_of_days_present = models.IntegerField(default=0)

    def __str__(self):
        return f"Name:{self.employee.fullName} |EmpID:{self.employee.empID} | Date:{self.date} | Status:{self.status}({self.time})"
