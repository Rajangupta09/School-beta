from django.db import models
from classform.models import ClassRoom, Subject
from employeeform.models import Teacher
# Create your models here.
class ClassRoomSubjectTeacher(models.Model):
	teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=True, null=True)
	class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE)