from django.db import models
from classform.models import ClassRoom, ClassRoomStudent, Subject
from fees.models import Session
from timetable.models import ClassRoomSubjectTeacher

class Exam(models.Model):
    examName = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return f"Exam :{self.examName}"


class ExamType(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, blank=True, null=True)
    examName = models.ForeignKey(Exam, on_delete=models.CASCADE, blank=True, null=True)
    examType = models.CharField(max_length=50, blank=True, null=True)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, blank=True, null=True)
    maxMarks = models.IntegerField(null = True, blank=True)
    priority = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return f"Exam :{self.examName.examName} ExamType:{self.examType}"


class ExamMapping(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, blank=True, null=True)
    examType = models.ForeignKey(ExamType, on_delete=models.CASCADE)
    minMarks = models.IntegerField(default=None, blank=True, null=True)
    maxMarks = models.IntegerField(default=100, blank=True)
    weightage = models.IntegerField(blank=True, null=True, default=None)
    classsubject = models.ForeignKey(ClassRoomSubjectTeacher, on_delete=models.CASCADE, default=None, null=True, blank=True)

    def __str__(self):
        return f"Exam:{self.examType.examName} ExamType:{self.examType.examType}|Subject:{self.classsubject.subject.name}"


class Marks(models.Model):
    classroomStudent = models.ForeignKey(
        ClassRoomStudent, on_delete=models.CASCADE)
    examName = models.ForeignKey(Exam, on_delete=models.CASCADE, null=True, blank=True, default=None)
    exam = models.ForeignKey(ExamMapping, on_delete=models.CASCADE)
    marks = models.IntegerField(default=None, blank=True, null=True)
    grade = models.CharField(max_length=5, blank=True, null=True)
    maxusermarks = models.IntegerField(default=0,blank=True, null=True)
    weightage = models.IntegerField(default=None, blank=True, null=True)
    remarks = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return f"{self.classroomStudent.student.fullName} | Exam:{self.exam.examType.examType} | Name: {self.examName.examName} | Subject:{self.exam.classsubject.subject.name}"


class AdditionalSubjectMapping(models.Model):
    examName = models.ForeignKey(Exam, on_delete=models.CASCADE)
    examType = models.ForeignKey(ExamType, on_delete=models.CASCADE)
    classroomStudent = models.ForeignKey(
        ClassRoomStudent, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    marks = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return f"{self.classroomStudent.student.fullName} | Exam:{self.examType.examType} {self.examName.examName} | Subject:{self.subject}"

class Skill(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, blank=True, null=True)
    skillType = models.CharField(max_length=100)
    skillCategory = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.skillType} | {self.skillCategory}"

class StudentSkill(models.Model):
    classroomStudent = models.ForeignKey(ClassRoomStudent, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    grade = models.CharField(max_length=10, blank=True)
    def __str__(self):
        return f"{self.classroomStudent.student.fullName} | Skill:{self.skill.skillType} {self.skill.skillCategory}"