from django.shortcuts import render, redirect
from .models import ClassRoomSubjectTeacher
from employeeform.models import Teacher
from classform.models import ClassRoom, Subject
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def add_detail(request):
    if request.method == 'POST':
        class_room = request.POST["class_room"]
        teacher_empID = request.POST["teacher_empID"]
        subject = request.POST["subject"]
        teachers = teacher_empID.split("-")
        subjects = subject.split("-")
        for i in range(0,len(subjects)-1):
            if subjects[i]:
                if not teachers[i] == '0':
                    tempvalid = ClassRoomSubjectTeacher.objects.filter(teacher=Teacher.objects.get(employee__empID=teachers[i]), class_room=ClassRoom.objects.get(classSection=class_room), subject=Subject.objects.get(name=subjects[i]))
                    if tempvalid:
                        messages.error(request, "Details Already exists!")
                        return redirect('/timetable/')
                    else:
                        ClassRoomSubjectTeacher.objects.create(teacher=Teacher.objects.get(employee__empID=teachers[i]), class_room=ClassRoom.objects.get(classSection=class_room), subject=Subject.objects.get(name=subjects[i]))
                else:
                    ClassRoomSubjectTeacher.objects.create(teacher=None, class_room=ClassRoom.objects.get(classSection=class_room), subject=Subject.objects.get(name=subjects[i]))
        messages.success(request, "Added detail!")
    return render(request, 'timetable/addDetail.html', {"class_rooms": ClassRoom.objects.all(), "teachers": Teacher.objects.all(), 'subjects': Subject.objects.all()})

@login_required
def view_details(request):
    class_room_subject_teachers = ClassRoomSubjectTeacher.objects.all().order_by('class_room_id')
    teacherswise = ClassRoomSubjectTeacher.objects.all().order_by('teacher_id')
    if request.method == "POST":
        if 'teacherid' in request.POST:
            teacherid = request.POST['teacherid']
            sub = request.POST['subject']
            class_sec = request.POST['class_room']
            temp = ClassRoomSubjectTeacher.objects.filter(teacher=Teacher.objects.get(employee__empID=teacherid), class_room=ClassRoom.objects.get(classSection=class_sec), subject=Subject.objects.get(name=sub))
            if not temp:
                ClassRoomSubjectTeacher.objects.create(teacher=Teacher.objects.get(employee__empID=teacherid), class_room=ClassRoom.objects.get(classSection=class_sec), subject=Subject.objects.get(name=sub))
                messages.success(request, "Added new Subject!")
            else:
                messages.warning(request, "Subject Already exist!")
            redirect('/timetable/viewTimeTableDetialsList')
        if 'classvalue' in request.POST:
            class_sec = request.POST['classvalue']
            sub = request.POST['subject']
            if 'teacher-value' in request.POST:
                teacherid = request.POST['teacher-value']
                temp =  ClassRoomSubjectTeacher.objects.filter(teacher=Teacher.objects.get(employee__empID=teacherid), class_room=ClassRoom.objects.get(classSection=class_sec), subject=Subject.objects.get(name=sub))
                if not temp:
                    ClassRoomSubjectTeacher.objects.create(teacher=Teacher.objects.get(employee__empID=teacherid), class_room=ClassRoom.objects.get(classSection=class_sec), subject=Subject.objects.get(name=sub))
                else:
                    messages.warning(request, "Subject Already exist!")
            else:
                ClassRoomSubjectTeacher.objects.create(teacher=None, class_room=ClassRoom.objects.get(classSection=class_sec), subject=Subject.objects.get(name=sub))
                messages.success(request, "Added new Subject!")
         
           
            redirect('/timetable/viewTimeTableDetialsList')
        if 'update' in request.POST:
            preclass = request.POST['preclass']
            presub = request.POST['presub']
            preteacher = request.POST['preteacher']
            newclass = request.POST['newclass']
            newsub = request.POST['newsub']
            newteacher = request.POST['newteacher']
            if preteacher == '0':
                updated = ClassRoomSubjectTeacher.objects.filter(class_room=ClassRoom.objects.get(classSection=preclass), subject=Subject.objects.get(name=presub)).last()
                updated.class_room = ClassRoom.objects.get(classSection=newclass)
                updated.subject = Subject.objects.get(name=newsub)
                if newteacher:
                    updated.teacher = Teacher.objects.get(employee__empID=newteacher)
                updated.save()
            else:
                updated = ClassRoomSubjectTeacher.objects.filter(teacher=Teacher.objects.get(employee__empID=preteacher), class_room=ClassRoom.objects.get(classSection=preclass), subject=Subject.objects.get(name=presub)).last()
                updated.class_room = ClassRoom.objects.get(classSection=newclass)
                updated.subject = Subject.objects.get(name=newsub)
                if newteacher:
                    updated.teacher = Teacher.objects.get(employee__empID=newteacher)
                updated.save()
            messages.success(request, 'Updated')
    if request.method == 'GET':
        if 'delete' in request.GET:
            preclass = request.GET.get('preclass')
            presub = request.GET.get('presub')
            preteacher = request.GET.get('preteacher')
            if not preteacher == '0':
                deleted = ClassRoomSubjectTeacher.objects.filter(teacher=Teacher.objects.get(employee__empID=preteacher), class_room=ClassRoom.objects.get(classSection=preclass), subject=Subject.objects.get(name=presub)).last()
                deleted.delete()
            else:
                deleted = ClassRoomSubjectTeacher.objects.filter(class_room=ClassRoom.objects.get(classSection=preclass), subject=Subject.objects.get(name=presub)).last()
                deleted.delete()
    
    return render(request, 'timetable/detailsList.html', {"teacherwise": teacherswise, "class_room_subject_teachers": class_room_subject_teachers, "class_rooms": ClassRoom.objects.all(), "teachers": Teacher.objects.all(), 'subjects': Subject.objects.all()})
