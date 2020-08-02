from django.shortcuts import render, redirect
from django.contrib import messages
from classform.models import ClassRoom, ClassRoomStudent
from .models import ClassNotice, StudentNotice
from accounts.models import UserProfile
from employeeform.models import Employee, Teacher
from django.contrib.auth.decorators import login_required
from timetable.models import ClassRoomSubjectTeacher
# Create your views here.

@login_required
def notice_home(request):
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
        class_section = request.POST.getlist("class_room")
        notice = request.POST.get("notice")
        document = request.FILES.get("noticeFile")
        for _class in class_section:
            ClassNotice.objects.create(classRoom=ClassRoom.objects.get(classSection=_class), notice=notice, notice_document=document)
        messages.success(request, 'Notice Posted Successfully.  ')
    return render(request, 'notice/noticeHome.html', context)

@login_required
def search_student(request):
    students = ClassRoomStudent.objects.all()
    class_rooms = ClassRoom.objects.all()
    if request.method == "GET":
        if "name" in request.GET:
            name = request.GET["name"]
            students = students.filter(student__fullName__icontains=name)
        if "class_room" in request.GET:
            classroom = request.GET.get("class_room")
            if not classroom == '':
                students = students.filter(classRoom__classSection=(classroom))
        if "addNumber" in request.GET:
            add_no = request.GET.get("addNumber")
            print(add_no)
            if not add_no == '':
                students = students.filter(student__admissionNumber=(add_no))

            if students:
                return render(request, 'notice/searchStudent.html', {"students": students, "values": request.GET, "class_rooms":class_rooms})
            else:
                messages.error(request, 'Cant find student with entered detail')
                return redirect('searchStudent')

    if request.method == "POST":
        add_no = request.POST.get("add_no")
        student = ClassRoomStudent.objects.get(student__admissionNumber=(add_no))
        notice = request.POST.get("notice")
        document = request.FILES.get("noticeFile")
        StudentNotice.objects.create(
            student=student, notice=notice, notice_document=document)
        messages.success(request, 'Notice Posted Succesfully.')

    return render(request, 'notice/searchStudent.html', {"class_rooms":class_rooms})



@login_required
def check_notice_student(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.user_type == "Student":
        addmission_number = user_profile.addmission_number
        notice = StudentNotice.objects.filter(student__student__admissionNumber=addmission_number)
        # notice = StudentNotice.objects.filter(student=student)
        if len(notice)>0:
            return render(request, 'notice/checkStudentNotice.html', {"notices":notice})
        else:
            return render(request, 'notice/checkStudentNotice.html')

@login_required
def past_notice_class(request):
    past_notice = ClassNotice.objects.all().order_by('-notice_date')
    value = 'Notice'
    if request.method == "GET":
        if 'search' in request.GET:
            value = request.GET['search']
            past_notice = past_notice.filter(notice__icontains=value)
        if 'sort' in request.GET:
            sort = request.GET['sort']
            if sort == 'OldestFirst':
                past_notice = past_notice.order_by('notice_date')
            elif sort == 'NewestFirst':
                past_notice = past_notice.order_by('-notice_date')
    return render(request, 'notice/pastNoticeClass.html', {'past_notice':past_notice, 'value' :value})

@login_required
def past_notice_student(request):
    past_notice = StudentNotice.objects.all().order_by('-notice_date')
    value = 'Notice'
    if request.method == "GET":
        if 'search' in request.GET:
            value = request.GET['search']
            past_notice = past_notice.filter(notice__icontains=value)
        if 'sort' in request.GET:
            sort = request.GET['sort']
            if sort == 'OldestFirst':
                past_notice = past_notice.order_by('notice_date')
            elif sort == 'NewestFirst':
                past_notice = past_notice.order_by('-notice_date')
    return render(request, 'notice/pastNoticeStudent.html', {'past_notice':past_notice, 'value' : value})

@login_required
def check_class_notice(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.user_type == "Student":
        addmission_number = user_profile.addmission_number
        student = ClassRoomStudent.objects.get(student__admissionNumber=addmission_number)
        class_room = student.classRoom
        notice = ClassNotice.objects.filter(classRoom=class_room)
        if len(notice)>0:
            return render(request, 'notice/checkClassNotice.html', {"notices":notice})
        else:
            return render(request, 'notice/checkClassNotice.html')

@login_required
def download_class_notice(request, pk):
    notice = ClassNotice.objects.get(id=pk)
    filename = notice.notice_document.split('/')[-1]
    response = HttpResponse(object_name.file, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response
