"""
Database tables for classform app
"""
from django.db import models
from form.models import StudentInfo, StudentRoute
from employeeform.models import Teacher
from datetime import datetime
from django.utils import timezone

# class ClassTable(models.Model):
#     """
#     Table for Class-Section
#     """
#     class_section = models.CharField(max_length=50)
#     def __str__(self):
#         return f"Class:{self.class_section}"


class ClassRoom(models.Model):
    """
    Table for Class Room details with Class-Section and Class Teacher Assigned
    """
    classSection = models.CharField(max_length=50)
    _class = models.CharField(max_length=50, blank=True)
    _section = models.CharField(max_length=50, blank=True)
    class_teacher_alloted = models.BooleanField(default=False)
    room_no = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Class:{self.classSection}"


def user_directory_path(instance, filename):
    """file will be uploaded to given path"""
    return 'report-card/{0}/{1}'.format(instance.class_room_student.student.admissionNumber, filename)


class ClassRoomStudent(models.Model):
    """
    Table for Student related to a classroom with roll number and student(foreign key) attributes
    """
    classRoom = models.ForeignKey(
        ClassRoom, on_delete=models.CASCADE, related_name='students')
    roll_number = models.IntegerField()
    student = models.OneToOneField(
        StudentInfo, on_delete=models.CASCADE, related_name='classroom_student')

    def __str__(self):
        return f"Class:{self.classRoom.classSection} | Student:{self.student.fullName} | Admission Number: {self.student.admissionNumber}"

    def save(self, *args, **kwargs):
        if len(ClassRoomStudent.objects.filter(classRoom=self.classRoom)) > 0:
            self.roll_number = ClassRoomStudent.objects.filter(
                classRoom=self.classRoom).last().roll_number + 1
        else:
            self.roll_number = 1
        return super(ClassRoomStudent, self).save(*args, **kwargs)


class Subject(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f"Name: {self.name} | Date: {self.date}"


class ReportCard(models.Model):
    """
    Table for Report Card for a class room student
    """
    class_room_student = models.ForeignKey(
        ClassRoomStudent, on_delete=models.CASCADE)
    reportCard = models.FileField(upload_to=user_directory_path)


class StudentRouteAttendence(models.Model):
    """
    Student Attendence table
    """
    student_route = models.ForeignKey(StudentRoute, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    date = models.DateField(default=timezone.now)
    time = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        unique_together = (('date', 'student_route'),)

    def __str__(self):
        return f"Name:{self.student_route.student.fullName}| Route:{self.student_route.shift.sub_route_code} | Date:{self.date} | Status:{self.status}"
