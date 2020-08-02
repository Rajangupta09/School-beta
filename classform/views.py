"""
  Handle class registration part
"""
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from employeeform.models import Teacher
from .models import ClassRoom, Subject, ClassRoomStudent
from django.contrib.auth.decorators import login_required


@login_required
def addclass(request):
    """
    Add new Class with teacher
    input: teacher name and class name
    """
    Class = ClassRoom.objects.all()
    if request.method == "POST":
        if 'update' in request.POST:
            _oldclass = request.POST.get('oldclass')
            _class = request.POST.get("newclass")
            _section = request.POST.get("newsection")
            room_no = request.POST.get("newroom")
            class_section = _class + "-" + _section
            oldclass = ClassRoom.objects.get(classSection=_oldclass)
            oldclass.classSection = class_section
            oldclass._class = _class
            oldclass._section = _section
            oldclass.room_no = room_no
            oldclass.save()
            return redirect('addClass')
        elif 'delete'in request.POST:
            _class = request.POST.get('oldclass')
            print(_class)
            students = ClassRoomStudent.objects.filter(classRoom__classSection=_class)
            print(students)
            if not students:
                try:
                    Classs = ClassRoom.objects.get(classSection=_class)
                    Classs.delete()
                    messages.success(request, 'Deleted Successfully')
                except:
                    messages.error(request, 'Couldnot Delete!')
            else:
                messages.error(request, 'Cannot Delete Students Exists!')
            return redirect('/classForm/Subject')
        else:
            _class = request.POST.get("class")
            _section = request.POST.get("section")
            room_no = request.POST.get("room_no")
            class_section = _class + "-" + _section
            class_rooms = ClassRoom.objects.filter(classSection=class_section)
            if len(class_rooms) > 0:
                messages.info(request, "Class already alloted")
                return redirect('addClass')
            classroom = ClassRoom.objects.create(
                classSection=class_section, _class=_class, _section=_section, room_no=room_no)
            classroom.save()
            messages.success(request, "Class alloted!")
            return redirect('addClass')

    return render(request, 'classform/addclass.html', {"Class": Class})


def addsubject(request):
    subjects = Subject.objects.all()

    if request.method == 'POST':
        if 'update' in request.POST:
            _oldsubject = request.POST.get('oldsub')
            _newsubject = request.POST.get('newsub')
            oldsubjects = Subject.objects.get(name=_oldsubject)
            date = oldsubjects.date
            oldsubjects.date = date
            oldsubjects.name = _newsubject
            oldsubjects.save()
            return redirect('/classForm/Subject')
        elif 'delete'in request.POST:
            _subject = request.POST.get('sub')
            subject = Subject.objects.get(name=_subject)
            subject.delete()
            return redirect('/classForm/Subject')
        else:
            _subject = request.POST.get('subject')
            subjectss = Subject.objects.filter(name=_subject)
            if subjectss:
                messages.warning(request, "Subject already alloted")
                return redirect('/classForm/Subject')
            subject = Subject.objects.create(name=_subject)
            subject.save()
            messages.success(request, "Subject allotted")
            return redirect('/classForm/Subject')

    return render(request, 'classform/addsubject.html', {'Subjects': subjects})
