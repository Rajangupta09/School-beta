from django.shortcuts import render, redirect
from django.http import HttpResponse

from classform.models import ClassRoom, Subject
from accounts.models import UserProfile
from classform.models import ClassRoomStudent
from timetable.models import ClassRoomSubjectTeacher
from employeeform.models import Employee, Teacher
from matplotlib import pyplot as plt
import numpy as np
import matplotlib
from markssection.models import ExamMapping
from .models import HomeWork, Syllabus
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages

matplotlib.use('Agg')
plt.style.use("fivethirtyeight")
# Create your views here.

@login_required
def homework_home(request):
    # subjects = (ExamMapping.objects.all().values('subject').distinct())
    subjects = Subject.objects.all()
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.user_type == "Teacher":
        emp_id = user_profile.emp_id
        employee = Employee.objects.get(empID=emp_id)
        teacher = Teacher.objects.get(employee=employee)
        class_section=teacher.classTeacher
        qs1 = ClassRoom.objects.filter(classroomsubjectteacher__teacher=teacher)
        qs2 = ClassRoomSubjectTeacher.objects.filter(teacher=teacher)
        class_rooms = qs1.union(qs2)
        context = {
        "class_rooms": class_rooms,
        "subjects":subjects
        }
    else:
        context = {
            "class_rooms": ClassRoom.objects.all(),
        "subjects":subjects
        }
    if request.method== "GET":
        if 'class' in request.GET:
            classval = request.GET.get('class')
            i = ''
            classval = classval.split(', ')
            for j in classval:
                classRoom=ClassRoomSubjectTeacher.objects.filter(class_room__classSection=j)
                for c in classRoom:
                    i+= c.subject.name + ', '
            return HttpResponse(i)
    
    if request.method == "POST":
        class_section = request.POST.getlist("class_room")
        subject = request.POST.get("subject")
        print(subject)
        print(class_section)
        description = request.POST.get("detail")
        document = request.FILES.get("homeworkFile")
        for c in class_section:
            classRoom = ClassRoomSubjectTeacher.objects.filter(class_room__classSection=c, subject__name=subject).last()
            if classRoom:
                temp = HomeWork.objects.filter(classRoom=classRoom, description=description, date_published=datetime.now())
                print(temp)
                if temp:
                    messages.warning(request, 'Already Exists!')
                else:
                    HomeWork.objects.create(classRoom=classRoom,description=description,
                                    date_published=datetime.now(), document=document)
                    messages.success(request, "Posted Successfully")
   
    return render(request, 'homework/addHomework.html', context)

@login_required
def check_homework(request):
    context = {
        "class_rooms": ClassRoom.objects.all(),
    }
    if request.method == "POST":
        class_section = request.POST.get("class_room")

        homeworks = HomeWork.objects.filter(
            classRoom=ClassRoom.objects.get(classSection=class_section))
        subjects = (ExamMapping.objects.all().values('subject').distinct())
        subjects_in_homework = []
        for homework in homeworks:
            sub = homework.subject
            if sub not in subjects_in_homework:
                subjects_in_homework.append(sub)

        y_axis = [1]*len(subjects_in_homework)
        print(subjects_in_homework)
        width = 0.1
        # y_axis = [1,1]
        subject_x = np.arange(1)
        print(len(subjects_in_homework))
        print("subject_x", subject_x)
        print("y_axis", y_axis)
        color = ["#444444", "#008fd5", "#349912",
                 "#876543", "#642111", "#076666"]
        for i in range(len(subjects_in_homework)):
            plt.bar(subject_x + width*i, y_axis, color=color[i], align='edge',
                    label=subjects_in_homework[i], width=width-0.02)
        # plt.xticks(subject_x, subjects_in_homework)
        plt.xticks([])

        # plt.bar(subject_x, y_axis, color="#444444",
        #         label="Mathematics", width=width)
        # plt.bar(subject_x+0.05+width, y_axis, color="#008fd5",
        #         label="English", width=width)
        plt.legend()
        plt.title(f"Chart for {class_section}")
        plt.xlabel("Subjects")
        # plt.ylabel("Marks")
        plt.tight_layout()
        plt.show()
        redirect('checkHomework')

    return render(request, 'homework/checkHomework.html', context)

@login_required
def syllabus(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.user_type == "Teacher":
        emp_id = user_profile.emp_id
        employee = Employee.objects.get(empID=emp_id)
        teacher = Teacher.objects.get(employee=employee)
        class_section=teacher.classTeacher
        qs1 = ClassRoom.objects.filter(classroomsubjectteacher__teacher=teacher)
        qs2 = ClassRoom.objects.filter(classSection=class_section)
        class_rooms = qs1.union(qs2)
        context = {
        "class_rooms": class_rooms
        }
    else:
        context = {
            "class_rooms": ClassRoom.objects.all()
        }
    if request.method == "POST":
        class_section = request.POST.get("class_room")
        description = request.POST.get("description")
        document = request.FILES.get("syllabus_file")
        Syllabus.objects.create(classRoom=ClassRoom.objects.get(classSection=class_section), description=description,
                                date_published=datetime.today(), document=document)
    return render(request, 'homework/syllabus.html', context)

@login_required
def past_syllabus(request):
    past_syllabus_ = Syllabus.objects.all()
    return render(request, 'homework/PastSyllabus.html', {'past_syllabus':past_syllabus_})

@login_required
def check_class_homework(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.user_type == "Student":
        addmission_number = user_profile.addmission_number
        student = ClassRoomStudent.objects.get(student__admissionNumber=addmission_number)
        class_room = student.classRoom
        homeworks = HomeWork.objects.filter(classRoom=class_room)
        if len(homeworks) > 0:
            return render(request, 'homework/studentClassHomework.html', {"homeworks":homeworks})
        else:
            return render(request, 'homework/studentClassHomework.html')

@login_required
def check_class_syllabus(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.user_type == "Student":
        addmission_number = user_profile.addmission_number
        student = ClassRoomStudent.objects.get(student__admissionNumber=addmission_number)
        class_room = student.classRoom
        syllabuss = Syllabus.objects.filter(classRoom=class_room)
        if len(syllabuss) > 0:
            return render(request, 'homework/checkSyllabus.html', {"syllabuss":syllabuss})
        else:
            return render(request, 'homework/checkSyllabus.html')

@login_required
def past_homework(request):
    class_view=True
    teacher_view=True
    date_view=True
    obj = {}
    timetable = ClassRoomSubjectTeacher.objects.all().order_by('teacher_id').exclude(teacher=None)
    past_homeworks = HomeWork.objects.all()
    if request.method=='GET':
        if 'class_room' in request.GET:
            class_room = request.GET.getlist('class_room')
            past_homeworks = HomeWork.objects.filter(classRoom__class_room__classSection__in=class_room)
            return render(request, 'homework/pastHomeWorks.html', {'past_homeworks':past_homeworks, 'timetable' : timetable, "class_rooms": ClassRoom.objects.all(), 'teachers': Teacher.objects.all(), 'cw': class_view})         
        if 'teachers' in request.GET:
            teacher = request.GET.getlist('teachers')
            timetable = ClassRoomSubjectTeacher.objects.filter(teacher_id__in=teacher).order_by('teacher_id').exclude(teacher=None)
            return render(request, 'homework/pastHomeWorks.html', {'past_homeworks':past_homeworks, 'timetable' : timetable, "class_rooms": ClassRoom.objects.all(), 'teachers': Teacher.objects.all(), 'tw': teacher_view})         
        if 'date' in request.GET:
            date = request.GET.get('date')
            if not date == '':
                date = date.split('-')
                print(date)
                past_homeworks = HomeWork.objects.filter(date_published__year=date[0], date_published__month=date[1])
                print(past_homeworks)
                return render(request, 'homework/pastHomeWorks.html', {'past_homeworks':past_homeworks, 'timetable' : timetable, "class_rooms": ClassRoom.objects.all(), 'teachers': Teacher.objects.all(), 'dw': date_view})         


    return render(request, 'homework/pastHomeWorks.html', {'past_homeworks':past_homeworks, 'timetable' : timetable, "class_rooms": ClassRoom.objects.all(), 'teachers': Teacher.objects.all(), 'cw': class_view, 'tw':teacher_view, 'dw':date_view})
