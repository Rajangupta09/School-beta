"""
Attendence app handling
"""
import io
import urllib
import base64
from datetime import date, datetime
import matplotlib
from matplotlib import pyplot as plt
from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import UserProfile
from employeeform.models import Teacher, Employee
from classform.models import ClassRoomStudent, ClassRoom
from .models import StudentAttendence, TeacherAttendence
from holiday.models import Holidays
from accounts.models import UserProfile
from collections import defaultdict
import pandas as pd
import numpy as np
import calendar
from django.contrib.auth.decorators import login_required
matplotlib.use('Agg')


@login_required
def student_attendence(request):
    """
    Handling student attendence
    Input: Admission Number or Class-Section
    Ouptut: List of students
    """

    # FOR DISPLAYING STUDENTS
    # for holidays in holiday_list:

    #     print(str(holidays), end="\n")
    #     if holidays == today:
    #         print('worked')
    # messages.danger(request, "Sorry You cannot mark attendence today!!")
    # return redirect('attendenceStudent')

    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.user_type == "Teacher":
        emp_id = user_profile.emp_id
        employee = Employee.objects.get(empID=emp_id)
        teacher = Teacher.objects.get(employee=employee)
        class_section = teacher.classTeacher
        classrooms = ClassRoom.objects.filter(classSection=class_section)
    else:
        classrooms = ClassRoom.objects.all()
    students = False
    if request.method == "GET":
        if "add_no" in request.GET:
            add_no = request.GET["add_no"]
            if add_no:
                students = ClassRoomStudent.objects.filter(
                    student__admissionNumber=add_no)
                request.session["add_no"] = add_no
            else:
                students = ClassRoomStudent.objects.all()
        if "class_room" in request.GET:
            class_name = request.GET["class_room"]
            if class_name:
                students = students.filter(
                    classRoom__classSection=class_name)
                request.session["class_name"] = class_name
        if students:
            today = date.today()
            holiday_list = Holidays.objects.filter(
                holiday_date=today, category='student')
            if holiday_list:
                messages.error(request, 'You cannot mark attendence today')
                return redirect('/attendence/student')

            return render(request, 'attendence/student.html', {"students": students, 'class_rooms': classrooms})

    # FOR MARKING ATTENDENCE

    if request.method == "POST":
        _date = date.today()
        if _date.weekday() == 6:
            messages.info(request, "Selected Date is a holiday!")
            return redirect('/attendence/student')
        classstudents = ClassRoomStudent.objects.filter(
            classRoom__classSection=request.session["class_name"])
        if "add_no" in request.session:
            classstudents = ClassRoomStudent.objects.filter(
                student__admissionNumber=request.session["add_no"])

        for classroomstudent in classstudents:
            if str(classroomstudent.student.admissionNumber) in request.POST:
                if StudentAttendence.objects.filter(student=classroomstudent).last():
                    current = StudentAttendence.objects.filter(
                        student=classroomstudent).last()
                    present = current.total_no_of_days_present
                    casual_leave = current.taken_casual_leave
                    sick_leave = current.taken_sick_leave
                    late = current.total_no_of_days_late
                else:
                    present = 0
                    casual_leave = 0
                    sick_leave = 0
                    late = 0
                s = StudentAttendence.objects.create(student=classroomstudent, date=_date, status=request.POST[str(
                    classroomstudent.student.admissionNumber)])
                if str(s.status) == "present":
                    s.total_no_of_days_present = present + 1
                    s.taken_casual_leave = casual_leave
                    s.taken_sick_leave = sick_leave
                    s.total_no_of_days_late = late
                if str(s.status) == "absent":
                    s.total_no_of_days_present = present
                    s.taken_casual_leave = casual_leave + 1
                    s.taken_sick_leave = sick_leave
                    s.total_no_of_days_late = late
                if str(s.status) == "leave":
                    s.total_no_of_days_present = present
                    s.taken_casual_leave = casual_leave
                    s.taken_sick_leave = sick_leave + 1
                    s.total_no_of_days_late = late
                if str(s.status) == "late":
                    s.total_no_of_days_present = present
                    s.taken_casual_leave = casual_leave
                    s.taken_sick_leave = sick_leave
                    s.total_no_of_days_late = late + 1
                s.save()
            messages.success(request, "Marked attendence")
    return render(request, 'attendence/student.html', {'class_rooms': classrooms})


@login_required
def student_attendence_report(request):
    if request.method == 'GET':
        return render(request, 'attendence/studentPieChart.html')
    try:
        report_data_query_set = None
        if 'year' in request.POST:
            report_data_query_set = StudentAttendence.objects.filter(
                date__year=request.POST['year'])
        if 'month' in request.POST:
            report_data_query_set = report_data_query_set.filter(
                date__month=request.POST['month'])
        if 'day' in request.POST:
            report_data_query_set = report_data_query_set.filter(
                date__day=request.POST['day'])

        if 'add_no' in request.POST and request.POST['add_no'] != '':
            report_data_query_set = report_data_query_set.filter(
                student__student__admissionNumber=request.POST['add_no'])
            present = 0
            absent = 0
            student_name = report_data_query_set[0].student.student.fullName

            for student in report_data_query_set:
                if student.status == "present":
                    present += 1
                else:
                    absent += 1
            slices = [present, absent]
            labels = ["Present", "Absent"]
            plt.clf()
            plt.pie(slices, labels=labels, startangle=90, autopct='%1.1f%%')
            plt.title(f"Attendence Report")
            plt.tight_layout()
            fig3 = plt.gcf()
            buf3 = io.BytesIO()
            fig3.savefig(buf3, format='png')
            buf3.seek(0)
            string = base64.b64encode(buf3.read())
            uri = 'data:image/png;base64,' + urllib.parse.quote(string)
            return render(request, 'attendence/studentPieChart.html', {'image': uri})
        else:
            report = defaultdict(list)

            class_rooms = set(
                [student.student.classRoom.classSection for student in report_data_query_set])
            for class_ in class_rooms:
                report[class_] = [0, 0, class_]

            for student in report_data_query_set:
                if student.status == "present":
                    report[student.student.classRoom.classSection][0] += 1
                else:
                    report[student.student.classRoom.classSection][1] += 1

            data_frame = pd.DataFrame.from_dict(report, orient="index", columns=[
                                                "Present", "Absent", "Class"])
            plt.clf()

            x = np.arange(len(class_rooms))  # the label locations
            width = 0.35  # the width of the bars

            fig, ax = plt.subplots()
            rects1 = ax.bar(
                x - width/2, data_frame['Present'], width, label='Present')
            rects2 = ax.bar(
                x + width/2, data_frame['Absent'], width, label='Absent')

# Add some text for labels, title and custom x-axis tick labels, etc.
            ax.set_ylabel('Attendence Score')
            ax.set_title('Attendence Report')
            ax.set_xticks(x)
            ax.set_xticklabels(class_rooms)
            ax.legend()

            def autolabel(rects):
                # Attach a text label above each bar in *rects*, displaying its height."""
                for rect in rects:
                    height = rect.get_height()
                    ax.annotate('{}'.format(height),
                                xy=(rect.get_x() + rect.get_width() / 2, height),
                                xytext=(0, 3),  # 3 points vertical offset
                                textcoords="offset points",
                                ha='center', va='bottom')

            autolabel(rects1)
            autolabel(rects2)

            fig.tight_layout()
            fig3 = plt.gcf()
            buf3 = io.BytesIO()
            fig3.savefig(buf3, format="png")
            buf3.seek(0)
            string = base64.b64encode(buf3.read())
            uri = "data:image/png;base64,"+urllib.parse.quote(string)
            return render(request, "attendence/studentPieChart.html", {"image": uri})
    except:
        return render(request, 'attendence/studentPieChart.html')


@login_required
def student_pie_chart(request):
    """
    Pie Chart using matplotlib
    Input: Month and Year for data required
    Output: Pie Chart
    """
    plt.style.use("fivethirtyeight")
    present = 0
    absent = 0
    leave = 0
    late = 0
    labels = ['Present', 'Absent', 'Leave', 'late']
    if request.method == "POST":
        _year = request.POST.get("year")
        student_attendence = StudentAttendence.objects.filter(
            date__year=_year)
        _month = request.POST.get("month")
        print(student_attendence)
        student_attendence = student_attendence.filter(date__month=_month)
        print(student_attendence)
        # user_profile = UserProfile.objects.get(user=request.user)
        # if user_profile.user_type != "Student":
        #     emp_id_no = user_profile.emp_id
        # else:
        admission_id_no = request.POST.get("add_no")
        print(admission_id_no)
        student_attendence = student_attendence.filter(
            student__student__admissionNumber=admission_id_no).last()
        print(student_attendence)
        if student_attendence:
            name = student_attendence.student.student.fullName
            present = student_attendence.total_no_of_days_present
            leave = student_attendence.taken_sick_leave
            absent = student_attendence.taken_casual_leave
            late = student_attendence.total_no_of_days_late
            total_days = student_attendence.total_no_of_days_present + student_attendence.taken_casual_leave + \
                student_attendence.taken_sick_leave + student_attendence.total_no_of_days_late
            slices = [present, absent, leave, late]
            plt.clf()
            plt.pie(slices, labels=labels, startangle=90, autopct='%1.1f%%')
            plt.title(f"Attendence Report")
            plt.tight_layout()
            fig3 = plt.gcf()
            buf3 = io.BytesIO()
            fig3.savefig(buf3, format='png')
            buf3.seek(0)
            string = base64.b64encode(buf3.read())
            uri = 'data:image/png;base64,' + urllib.parse.quote(string)
            return render(request, 'attendence/studentPieChart.html', {'image': uri, 'student_detail': student_attendence, 'total': total_days})
        else:
            messages.warning(request, 'No Record Found')
            redirect('/piechartStudent')
    return render(request, 'attendence/studentPieChart.html')


@login_required
def student_total_report(request):
    classrooms = ClassRoom.objects.all()
    cal = calendar.Calendar()
    cal.setfirstweekday(6)
    error = 'No Record Found...'
    if request.method == "GET":
        try:
            if 'year' in request.GET:
                _year = request.GET.get('year')
                student_attendence = StudentAttendence.objects.filter(
                    date__year=_year).order_by('student')
                holiday_list = Holidays.objects.filter(
                    holiday_date__year=_year)
            if 'month' in request.GET:
                _month = request.GET.get('month')
                student_attendence = student_attendence.filter(
                    date__month=_month)
                holiday_list = holiday_list.filter(holiday_date__month=_month)
            if "class" in request.GET:
                _class = request.GET.get("class")
                student_attendence = student_attendence.filter(
                    student__classRoom__classSection=_class)
                holiday_list = holiday_list.filter(studentholiday=_class)
            month_days = cal.itermonthdays(int(_year), int(_month))
            days = []
            for day in month_days:
                days.append(int(day))
            month = calendar.month_name[int(_month)]
            if student_attendence:
                holiday = []
                for h in holiday_list:
                    holiday.append(h.holiday_date.day)
                li = {}
                for student in student_attendence:
                    li.update(
                        {student.student.student.admissionNumber: student.student.student.fullName})
                dic = {}
                for item in li:
                    student = student_attendence.filter(
                        student__student__admissionNumber=item)
                    present = []
                    absent = []
                    leave = []
                    late = []
                    for t in student:
                        if t.status == 'present':
                            present.append(t.date.day)
                        elif t.status == 'absent':
                            absent.append(t.date.day)
                        elif t.status == 'leave':
                            leave.append(t.date.day)
                        elif t.status == 'late':
                            late.append(t.date.day)

                    total = (len(present) / (len(present) +
                                             len(absent)+len(leave)+len(late))) * 100
                    dic.update({item: {'name': li[item], 'present': present,
                                       'absent': absent, 'leave': leave, 'late': late, 'total': total}})

                return render(request, 'attendence/studentAdmin.html', {'days': days, 'employees': dic, 'holidays': holiday, 'year': _year, 'month': month, 'class_rooms': classrooms, 'classroom': _class})
            else:
                messages.error(request, "No Record Found...")
                return render(request, 'attendence/studentAdmin.html', {'employee': error, 'year': _year, 'month': month, 'days': days, 'class_rooms': classrooms})
        except:
            return render(request, 'attendence/studentAdmin.html', {'class_rooms': classrooms})


@login_required
def teacher_attendence(request):
    """
    Handling teacher attendence
    Input: EmpID Number or Teacher Name
    Ouptut: List of Teachers
    """
    # FOR DISPLAYING TEACHERS
    employee = False
    if request.method == "GET":
        if "emp_id" in request.GET:
            emp_id = request.GET["emp_id"]
            if emp_id:
                request.session["emp_id"] = emp_id
                employee = Employee.objects.filter(empID__contains=emp_id)
            else:
                employee = Employee.objects.all()
        if "teacher_name" in request.GET:
            teacher_name = request.GET["teacher_name"]
            if teacher_name:
                request.session["teacher_name"] = teacher_name
                employee = employee.filter(fullName__icontains=teacher_name)
        if "Category" in request.GET:
            Category = request.GET["Category"]
            if Category:
                request.session["Category"] = Category
                employee = employee.filter(empCategory__icontains=Category)
        if employee:
            today = date.today()
            holiday_list = Holidays.objects.exclude(category='student')
            holiday_list = holiday_list.filter(holiday_date=today)
            if holiday_list:
                messages.error(request, 'You cannot mark attendence today')
                return redirect('/attendence/employee-attendence')
            return render(request, 'attendence/teacher.html', {"employee": employee})
    # FOR MARKING ATTENDENCE
    if request.method == "POST":
        _date = date.today()
        if _date.weekday() == 6:
            messages.info(request, "Selected Date is a holiday!")
            return redirect('/attendence/employee-attendence')
            exit()
        employee = Employee.objects.filter(
            empID__icontains=request.session['emp_id'])
        if "teacher_name" in request.session:
            employee = Employee.objects.filter(
                fullName__icontains=request.session['teacher_name'])
        if "Category" in request.session:
            employee = Employee.objects.filter(
                empCategory__icontains=request.session['Category'])
        for emp in employee:
            if str(emp.empID) in request.POST:
                if TeacherAttendence.objects.filter(employee=emp).last():
                    current = TeacherAttendence.objects.filter(
                        employee=emp).last()
                    present = current.total_no_of_days_present
                    casual_leave = current.taken_casual_leave
                    sick_leave = current.taken_sick_leave
                else:
                    present = 0
                    casual_leave = 0
                    sick_leave = 0

                s = TeacherAttendence.objects.create(
                    employee=emp, date=_date, status=request.POST[str(emp.empID)])
                if str(s.status) == "present":
                    s.total_no_of_days_present = present + 1
                    s.taken_casual_leave = casual_leave
                    s.taken_sick_leave = sick_leave
                if str(s.status) == "absent":
                    s.total_no_of_days_present = present
                    s.taken_casual_leave = casual_leave + 1
                    s.taken_sick_leave = sick_leave
                if str(s.status) == "leave":
                    s.total_no_of_days_present = present
                    s.taken_casual_leave = casual_leave
                    s.taken_sick_leave = sick_leave + 1
                s.save()
        messages.success(request, "Marked attendence")
    return render(request, 'attendence/teacher.html')


@login_required
def teacher_pie_chart(request):
    """
    Pie Chart using matplotlib
    Input: Month and Year for data required
    Output: Pie Chart
    """
    plt.style.use("fivethirtyeight")
    present = 0
    absent = 0
    leave = 0
    labels = ['Present', 'Absent', 'Leave']
    if request.method == "POST":
        _year = request.POST.get("year")
        teacher_attendence = TeacherAttendence.objects.filter(
            date__year=_year)
        _month = request.POST.get("month")
        teacher_attendence = teacher_attendence.filter(date__month=_month)
        # user_profile = UserProfile.objects.get(user=request.user)
        # if user_profile.user_type != "Student":
        #     emp_id_no = user_profile.emp_id
        # else:
        emp_id_no = request.POST.get("emp_id_no")
        emp_att = teacher_attendence.filter(employee_id=emp_id_no).last()
        if emp_att:
            name = emp_att.employee.fullName
            present = emp_att.total_no_of_days_present
            leave = emp_att.taken_sick_leave
            absent = emp_att.taken_casual_leave
            total_days = emp_att.total_no_of_days_present + \
                emp_att.taken_casual_leave + emp_att.taken_sick_leave
            slices = [present, absent, leave]
            plt.clf()
            plt.pie(slices, labels=labels, startangle=90, autopct='%1.1f%%')
            plt.title(f"Attendence Report")
            plt.tight_layout()
            fig3 = plt.gcf()
            buf3 = io.BytesIO()
            fig3.savefig(buf3, format='png')
            buf3.seek(0)
            string = base64.b64encode(buf3.read())
            uri = 'data:image/png;base64,' + urllib.parse.quote(string)
            return render(request, 'attendence/teacherPieChart.html', {'image': uri, 'emp_detail': emp_att, 'total': total_days})
        else:
            messages.warning(request, 'No Record Found')
            redirect('/piechartTeacher')
    return render(request, 'attendence/teacherPieChart.html')


@login_required
def employee_total_report(request):
    cal = calendar.Calendar()
    cal.setfirstweekday(6)
    error = 'No Record Found...'
    if request.method == "GET":
        try:
            if 'year' in request.GET:
                _year = request.GET.get('year')
                teacher_attendence = TeacherAttendence.objects.filter(
                    date__year=_year).order_by('employee')
                holiday_list = Holidays.objects.filter(
                    holiday_date__year=_year)
            if 'month' in request.GET:
                _month = request.GET.get('month')
                teacher_attendence = teacher_attendence.filter(
                    date__month=_month)
                holiday_list = holiday_list.filter(holiday_date__month=_month)
            if "category" in request.GET:
                _category = request.GET.get("category")
                teacher_attendence = teacher_attendence.filter(
                    employee_empCategory__icontains=_category)
                holiday_list = holiday_list.filter(employeeholiday=_category)

            month_days = cal.itermonthdays(int(_year), int(_month))
            days = []
            for day in month_days:
                days.append(int(day))
            month = calendar.month_name[int(_month)]
            if teacher_attendence:
                holiday = []
                for h in holiday_list:
                    holiday.append(h.holiday_date.day)
                li = {}
                for teacher in teacher_attendence:
                    li.update({teacher.employee_id: teacher.employee.fullName})
                dic = {}
                for item in li:
                    teacher = teacher_attendence.filter(employee_id=item)
                    present = []
                    absent = []
                    leave = []
                    late = []
                    for t in teacher:
                        if t.status == 'present':
                            present.append(t.date.day)
                        elif t.status == 'absent':
                            absent.append(t.date.day)
                        elif t.status == 'leave':
                            leave.append(t.date.day)
                        elif t.status == 'late':
                            late.append(t.date.day)
                    total = (len(present) / (len(present) +
                                             len(absent)+len(leave)+len(late))) * 100
                    dic.update({item: {'name': li[item], 'present': present,
                                       'absent': absent, 'leave': leave, 'late': late, 'total': total}})

                return render(request, 'attendence/employeeAdmin.html', {'days': days, 'employees': dic, 'holidays': holiday, 'year': _year, 'month': month})
            else:
                messages.error(request, "No Record Found...")
                return render(request, 'attendence/employeeAdmin.html', {'employee': error, 'year': _year, 'month': month, 'days': days})
        except:
            return render(request, 'attendence/employeeAdmin.html')
