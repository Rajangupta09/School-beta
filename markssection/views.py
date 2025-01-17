import io
import urllib, base64
import matplotlib
matplotlib.use('Agg')
import numpy as np
from tempfile import NamedTemporaryFile
from django.core import serializers

from django.core.files import File
from openpyxl import load_workbook
import matplotlib.pyplot as plt
from django.shortcuts import render, redirect, get_object_or_404
from .models import ExamType, Exam, ExamMapping, Marks, AdditionalSubjectMapping, Skill, StudentSkill
from employeeform.models import Teacher, Employee
from classform.models import ClassRoom, ClassRoomStudent, ReportCard
from attendence.models import StudentAttendence, TeacherAttendence
from fees.models import Session
from timetable.models import ClassRoomSubjectTeacher
from django.http import HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from accounts.models import UserProfile
from django.contrib.auth.decorators import login_required




@login_required
def add_exam_form(request):
    """
    Add exams for eg. UT-1, SA-1.
    Input: Exam Name and Description
    """
    if request.method == "POST":
        if "exam_name" in request.POST:
            exam_name = request.POST["exam_name"]
        if "description" in request.POST:
            description = request.POST["description"]
        temp = Exam.objects.filter(examName=exam_name)
        if not temp:
            Exam.objects.create(examName=exam_name, description=description)
            return HttpResponse('1')

    if request.method == 'GET':
        if 'did' in request.GET:
            _id = request.GET.get('did')
            exam_ = Exam.objects.get(id=_id)
            exam_.delete()

        if 'id' in request.GET:
            _id = request.GET.get('id')
            _name = request.GET.get('name')
            _desc = request.GET.get('desc')
            exam = Exam.objects.get(id=_id)
            exam.examName = _name
            exam.description = _desc
            exam.save() 
    return render(request, 'marks/home.html', {"exams": Exam.objects.all().order_by('id')})

@login_required
def exam_type_form(request):
    """
    Add Exam Type like Oral , Practical, Theory
    Input: Exam Name, Exam Type Name, Min/Max Marks, Priority
    """
    context = {
        "class_rooms": ClassRoom.objects.all(),
        "exam_types": ExamType.objects.all(),
        "exam_names": Exam.objects.all(),
        "sessions" : Session.objects.all(),
        "subjects": ClassRoomSubjectTeacher.objects.all().values('subject').distinct(),
        "examtypes" : ExamType.objects.all().order_by('id')
    }

    if request.method == "POST":
        description = None
        if "session" in request.POST:
            session = request.POST["session"]
        if "classroom" in request.POST:
            classroom = request.POST.getlist("classroom")
        if "description" in request.POST:
            description = request.POST["description"]
        if "priority" in request.POST:
            priority = request.POST["priority"]
        if "exam_name" in request.POST:
            exam_name = request.POST["exam_name"]
        if "exam_type" in request.POST:
            exam_type = request.POST["exam_type"]
        
        for c in classroom:
            ExamType.objects.create(
                            examName=Exam.objects.get(examName=exam_name),
                            examType=exam_type,
                            priority=priority,
                            session = Session.objects.get(name=session),
                            classroom=ClassRoom.objects.get(classSection=c),     
                            description = description
                            )
            messages.success(request, 'Uploaded Successfully!')
        redirect('/addExamType')
        # except:
        #     messages.error(request, 'Couldnot Upload!')

    if request.method == 'GET':
        if 'deid' in request.GET:
            deid = request.GET.get('deid')
            exam = ExamType.objects.get(id=deid)
            exam.delete()

        if 'eid' in request.GET:
            eid = request.GET.get('eid') 
            print(eid)
            session = request.GET.get('session')
            ename = request.GET.get('ename')
            print(ename)
            etype = request.GET.get('etype')
            eclass = request.GET.get('eclass')
            priority = request.GET.get('priority')
            description = request.GET.get('description')
            exam = ExamType.objects.get(id=eid)
            exam.examName=Exam.objects.get(examName=ename)
            exam.examType=etype
            exam.priority=priority
            exam.session = Session.objects.get(name=session)
            exam.classroom=ClassRoom.objects.get(classSection=eclass)     
            exam.description = description
            exam.save()
            return render(request, 'marks/examType.html', context)


    return render(request, 'marks/examType.html', context)

@login_required
def exam_mapping(request):
    """
    Map exam type with Exam Name eg. SA-1 mapped with Theory
    Input: Subject, ClassRoom, Exam Name & Type
    """
    if request.method == "GET":
        if 'classs' in request.GET:
            classs = request.GET.get('classs')
            li = []
            subject = ClassRoomSubjectTeacher.objects.filter(class_room__classSection=classs)
            for sub in subject:
                li.append(sub.subject.name + ',')
            return HttpResponse(li)

    if request.method == "POST":
        if "session" in request.POST:
            session = request.POST["session"]
        if "exam_type" in request.POST:
            exam_type = request.POST["exam_type"]
        if "subject" in request.POST:
            subject = request.POST.getlist("subject")
        if "max_marks" in request.POST:
            max_marks = request.POST["max_marks"]
        if "min_marks" in request.POST:
            min_marks = request.POST["min_marks"]
        if "weightage" in request.POST:
            weightage = request.POST["weightage"]
        if "class_room" in request.POST:
            class_room = request.POST.getlist("class_room")
            for classs in class_room:
                for sub in subject:
                    temp =  ExamMapping.objects.filter(classsubject= ClassRoomSubjectTeacher.objects.get(class_room__classSection=classs, subject__name=sub), session= Session.objects.get(id=session), examType=ExamType.objects.get(examType=exam_type, classroom__classSection=classs))
                    if not temp:
                        ExamMapping.objects.create(classsubject= ClassRoomSubjectTeacher.objects.get(class_room__classSection=classs, subject__name=sub),minMarks=min_marks, maxMarks=max_marks, weightage=weightage,
                                    session= Session.objects.get(id=session),
                                    examType=ExamType.objects.get(examType=exam_type, classroom__classSection=classs))
                        students=ClassRoomStudent.objects.filter(classRoom__classSection=classs)

                        for stu in students:
                            print(stu)
                            temp = Marks.objects.filter(classroomStudent=stu, exam=ExamMapping.objects.last())
                            if not temp:
                                exam = ExamMapping.objects.last()
                                Marks.objects.create(classroomStudent=stu, exam=exam, examName=exam.examType.examName ,marks=None, grade=None, maxusermarks=None, weightage=None, remarks=None)
                        messages.success(request, 'Exam Mapped Successfully.')
                    else:
                        messages.warning(request,'Already exists.')
                    
        
        return redirect('examMapping')

    context = {
        "sessions": Session.objects.all(),
        "class_rooms": ClassRoom.objects.all(),
        "exam_types": ExamType.objects.all(),
        "exammap": ExamMapping.objects.all(),
        "subjects": ClassRoomSubjectTeacher.objects.all().values('subject').distinct()
    }
    return render(request, 'marks/examMapping.html', context)

@login_required
def add_marks(request):
    """
    Register marks for students
    Input: ClassName, Exam Type and Exam Name, Subject
    Output: A list of students in a classroom and multiple input field for entering marks
    """



    exam_names = Exam.objects.all()
    sessions = Session.objects.all()
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.user_type == "Teacher":
        emp_id = user_profile.emp_id
        employee = Employee.objects.get(empID=emp_id)
        teacher = Teacher.objects.get(employee=employee)
        class_section=teacher.classTeacher
        class_rooms= ClassRoom.objects.filter(classSection=class_section)
    else:
       class_rooms = ClassRoom.objects.all()

    if request.method == "GET":
        if 'bid' in request.GET:
            bid = request.GET.get('bid')
            bmark = request.GET.get('marks')
            bid = bid.split(',')
            print(bid)
            bmark = bmark.split(',')
            for i in range(0,((len(bid))-1)):
                print(bmark[i], bid[i])
                mark = Marks.objects.get(id=bid[i])
                mark.marks=bmark[i]
                mark.save()
            return HttpResponse('Success')


        if 'tclass' in request.GET:
            tclass = request.GET.get('tclass')
            exam_types = ExamType.objects.filter(classroom__classSection=tclass)
            li = ''
            for e in exam_types:
                li += e.examType + ','
            return HttpResponse(li)

        if 'deleteid' in request.GET:
            deleteid = request.GET.get('deleteid')
            dele = Marks.objects.get(id=deleteid)
            dele.delete()
            return HttpResponse('deleted')
        if 'mid' in request.GET:
            print('qwerty')
            mid = request.GET.get('mid')
            mark = Marks.objects.get(id=mid)
            marks = request.GET.get('marks')
            print(marks)
            if not marks == '' or mark.marks == marks:
                mark.marks=marks
            grade = request.GET.get('grade') 
            if not grade == '' or mark.grade == grade:
                mark.grade=grade
            maxusermarks = request.GET.get('maxusermarks')
            if not maxusermarks == '' or mark.maxusermarks == maxusermarks:
                mark.maxusermarks=maxusermarks 
            weightage = request.GET.get('weightage') 
            if not weightage == '' or mark.weightage == weightage:
                mark.weightage=weightage
            remarks = request.GET.get('remarks')
            if not remarks == '' or mark.remarks == remarks:
                mark.remarks=remarks
            mark.save()
            print('hello')
            return HttpResponse('Success')

        if "session" in request.GET:
            session = request.GET["session"]
            request.session["session"] = session
        if "class_name" in request.GET:
            class_name = request.GET["class_name"]
            request.session["class_name"] = class_name
        if "exam_type" in request.GET:
            exam_type = request.GET["exam_type"]
            request.session["exam_type"] = exam_type
            print(exam_type)
            exams = Marks.objects.filter(exam__session__id=session,exam__classsubject__class_room__classSection=class_name,exam__examType__examType=exam_type).order_by('classroomStudent')
            print(exams)
            return render(request, 'marks/addMarks.html', {"exams": exams})
            # except:
            #     messages.error(request, "Class doesn't exist")
            #     redirect('addMarks')

       



    return render(request, 'marks/addMarks.html', {"sessions":sessions, "exam_types":ExamType.objects.all(),
                                                   "class_rooms": class_rooms, "values": request.GET, "exam_names": exam_names})

@login_required
def additional_sub_mapping(request):
    """
    Add additional subject for each student "
    Input: Admission Number, Exam Name and Type, Subject Name, Marks
    """
    if request.method == "POST":
        print(request.POST)
        if "add_number" in request.POST:
            add_number = request.POST["add_number"]
        if "exam_name" in request.POST:
            exam_name = request.POST["exam_name"]
        if "exam_type" in request.POST:
            exam_type = request.POST["exam_type"]
        if "subject" in request.POST:
            subject = request.POST["subject"]
        if "marks" in request.POST:
            marks = request.POST["marks"]

        _student = ClassRoomStudent.objects.get(
            student__admissionNumber=add_number)
        exam_name = Exam.objects.get(examName=exam_name)
        exam_type = ExamType.objects.get(examType=exam_type)
        AdditionalSubjectMapping.objects.create(examName=exam_name,
                                                examType=exam_type,
                                                classroomStudent=_student,
                                                marks=marks,
                                                subject=subject)

        return HttpResponse('')

@login_required
def addSkills(request):
    if request.method== 'POST':
        if "session" in request.POST:
            session = request.POST["session"]
            request.session["session"] = session
        if "skillType" in request.POST:
            skillType = request.POST["skillType"]
            request.session["skillType"] = skillType
        if "skillCategory" in request.POST:
            skillCategory = request.POST["skillCategory"]
            request.session["skillCategory"] = skillCategory
        if "edit-id" in request.POST:
            edit = request.POST["edit-id"]
            if not len(edit) == 0:
                skilll = Skill.objects.get(id=edit)
                skilll.session = Session.objects.get(id=session)
                skilll.skillType = skillType
                skilll.skillCategory = skillCategory
                skilll.save()
                messages.success(request, 'data Updated Successfully.')
            else:
                temp = Skill.objects.filter(session__id=session, skillType__iexact=skillType, skillCategory__iexact=skillCategory)
                if not temp:
                    Skill.objects.create(session = Session.objects.get(id=session), skillType=skillType, skillCategory=skillCategory)
                    messages.success(request, 'uploaded Successfully!')
                else:
                    messages.warning(request, 'Already exists!')
            
    return render(request, 'marks/skill.html', {"skills": Skill.objects.all(),"sessions": Session.objects.all()})


@login_required
def Skills(request):
    students = ClassRoomStudent.objects.all()
    skills = Skill.objects.all()
    for student in students:
        for skill in skills:
            temp = StudentSkill.objects.filter(classroomStudent = student, skill=skill)
            if not temp:
                StudentSkill.objects.create(classroomStudent = student, skill=skill)


    if request.method == 'GET':
        if 'mid' in request.GET:
            mid = request.GET.get('mid')
            grade = request.GET.get('value')
            stu = StudentSkill.objects.get(id=mid)
            stu.grade = grade
            stu.save()
            return HttpResponse('Successful')
        if "session" in request.GET:
            session = request.GET["session"]
            request.session["session"] = session
        if "class_name" in request.GET:
            class_name = request.GET["class_name"]
            request.session["class_name"] = class_name
            skills = StudentSkill.objects.filter(classroomStudent__classRoom__classSection=class_name, skill__session__id=session).order_by('classroomStudent')
            
            return render(request, 'marks/addSkills.html', {"skills":skills, "sessions": Session.objects.all(), "class_rooms": ClassRoom.objects.all()})
    return render(request, 'marks/addSkills.html', {"sessions": Session.objects.all(), "class_rooms": ClassRoom.objects.all()})



@login_required
def report_card(request):
    """
    Report Card for stduent by searching admission number
    Issue: Formating of excell sheet get's overlapped
    """
    if request.method == "POST":
        class_room = request.POST.get("class_room")
        pk = request.POST.get("add_number")
        if pk and class_room:
            class_room_student = ClassRoomStudent.objects.get(
                student__admissionNumber=pk)
            additional_sub = AdditionalSubjectMapping.objects.filter(
                classroomStudent=class_room_student)[0].subject
            class_room = class_room
            marks = Marks.objects.filter(classroomStudent=class_room_student)
            subjects = []
            exam_mapping = ExamMapping.objects.filter(classroom=class_room)

            # get subjects
            for a in exam_mapping:
                if a.subject not in subjects:
                    subjects.append(a.subject)
            subjects.sort()

            # get marks for unit test, note-book, half-yearly, SEA exam
            ut_1_marks_list = []
            exam_name = Exam.objects.get(examName='UT-1')
            marks_ut_1 = marks.filter(
                examName=exam_name, classRoomStudent=class_room_student)
            for sub in subjects:
                ut_1_marks_list.append(marks_ut_1.get(subject=sub).marks)

            ut_1_marks_list.append(AdditionalSubjectMapping.objects.get(
                subject=additional_sub, classroomStudent=class_room_student, examName=exam_name).marks)

            ut_2_marks_list = []
            exam_name = Exam.objects.get(examName='UT-2')
            marks_ut_2 = marks.filter(
                examName=exam_name, classRoomStudent=class_room_student)
            for sub in subjects:
                ut_2_marks_list.append(marks_ut_2.get(subject=sub).marks)

            ut_2_marks_list.append(AdditionalSubjectMapping.objects.get(
                subject=additional_sub, classroomStudent=class_room_student, examName=exam_name).marks)

            annual_term_marks_list = []
            exam_name = Exam.objects.get(examName='Annual')
            marks_annual_term = marks.filter(
                examName=exam_name, classRoomStudent=class_room_student)
            for sub in subjects:
                annual_term_marks_list.append(
                    marks_annual_term.get(subject=sub).marks)

            annual_term_marks_list.append(AdditionalSubjectMapping.objects.get(
                subject=additional_sub, classroomStudent=class_room_student, examName=exam_name).marks)

            half_yearly_marks_list = []
            exam_name = Exam.objects.get(examName='Half-Yearly')
            marks_half_yearly = marks.filter(
                examName=exam_name, classRoomStudent=class_room_student)
            for sub in subjects:
                half_yearly_marks_list.append(
                    marks_half_yearly.get(subject=sub).marks)

            half_yearly_marks_list.append(AdditionalSubjectMapping.objects.get(
                subject=additional_sub, classroomStudent=class_room_student, examName=exam_name).marks)

            sea1_term_marks_list = []
            exam_name = Exam.objects.get(examName='SEA-1')
            marks_sea1_term = marks.filter(
                examName=exam_name, classRoomStudent=class_room_student)
            for sub in subjects:
                sea1_term_marks_list.append(
                    marks_sea1_term.get(subject=sub).marks)

            sea1_term_marks_list.append(AdditionalSubjectMapping.objects.get(
                subject=additional_sub, classroomStudent=class_room_student, examName=exam_name).marks)

            sea2_term_marks_list = []
            exam_name = Exam.objects.get(examName='SEA-2')
            marks_sea2_term = marks.filter(
                examName=exam_name, classRoomStudent=class_room_student)
            for sub in subjects:
                sea2_term_marks_list.append(
                    marks_sea2_term.get(subject=sub).marks)

            sea2_term_marks_list.append(AdditionalSubjectMapping.objects.get(
                subject=additional_sub, classroomStudent=class_room_student, examName=exam_name).marks)

            notebook_1_marks_list = []
            exam_name = Exam.objects.get(examName='NoteBook-1')
            marks_notebook_1 = marks.filter(
                examName=exam_name, classRoomStudent=class_room_student)
            for sub in subjects:
                notebook_1_marks_list.append(
                    marks_notebook_1.get(subject=sub).marks)

            notebook_1_marks_list.append(AdditionalSubjectMapping.objects.get(
                subject=additional_sub, classroomStudent=class_room_student, examName=exam_name).marks)

            notebook_2_marks_list = []
            exam_name = Exam.objects.get(examName='NoteBook-2')
            marks_notebook_2 = marks.filter(
                examName=exam_name, classRoomStudent=class_room_student)
            for sub in subjects:
                notebook_2_marks_list.append(
                    marks_notebook_2.get(subject=sub).marks)

            notebook_2_marks_list.append(AdditionalSubjectMapping.objects.get(
                subject=additional_sub, classroomStudent=class_room_student, examName=exam_name).marks)

            subjects.append(additional_sub)

            if "excel" in request.FILES:
                excel_file = request.FILES["excel"]

                wb = load_workbook(excel_file)
                sheet = wb.get_sheet_by_name('ANNUAL')

                # set name, parents name, dob, addmission number, class, attendence
                sheet["B9"] = class_room_student.student.fullName
                sheet["B11"] = class_room_student.student.admissionNumber
                sheet["B10"] = class_room_student.student.parent.fatherName
                sheet["L10"] = class_room_student.student.parent.motherName
                sheet["K9"] = class_room_student.roll_number
                sheet["B12"] = class_room_student.student.dob
                sheet["G9"] = class_room_student.classRoom.classSection

                # get total attendence data
                total_days = StudentAttendence.objects.filter(
                    student=class_room_student).count()
                present_days = StudentAttendence.objects.filter(
                    student=class_room_student, status="present").count()
                sheet["L11"] = present_days
                sheet["N11"] = total_days

                for i in range(len(subjects)):
                    sheet[f'A{i+17}'].value = subjects[i]
                    sheet[f'B{i+17}'].value = ut_1_marks_list[i]
                    sheet[f'C{i+17}'].value = sea1_term_marks_list[i]
                    sheet[f'D{i+17}'].value = half_yearly_marks_list[i]

                    sheet[f'G{i+17}'].value = subjects[i]
                    sheet[f'H{i+17}'].value = ut_2_marks_list[i]
                    sheet[f'I{i+17}'].value = sea2_term_marks_list[i]
                    sheet[f'J{i+17}'].value = annual_term_marks_list[i]

                sheet.delete_rows(16+len(subjects), 9 - len(subjects))
                # wb.save('report-card.xlsx')
                with NamedTemporaryFile() as tmp:
                    wb.save(tmp.name)
                    tmp.seek(0)

                    report_card = ReportCard.objects.create(class_room_student=class_room_student)
                    report_card.reportCard.save("reportcard",File(tmp), True)
                    report_card.save()

                    try:
                        from win32com import client
                        import win32api

                        excel = client.DispatchEx("Excel.Application")
                        excel.Visible = 0

                        wb = excel.Workbooks.Open(tmp)
                        ws = wb.Worksheets[1]
                        try:
                            wb.SaveAs('c:\\targetfolder\\feeslip.pdf', FileFormat=57)
                        except:
                            print ("Failed to convert")
                        finally:
                            wb.Close()
                            excel.Quit()
                    except:
                        pass

    return render(request, 'marks/reportCard.html')

@login_required
def report_analysis(request):
    """
    Generate graph for SA's and UT's for a given student
    Input: Student's Admission Number
    Output: Bar graph for a given term or combined term with all UT's and SA's
    """
    if request.method == 'GET':
        plt.style.use("fivethirtyeight")
        if "add_number" in request.GET:
            add_number = request.GET["add_number"]
        if "term" in request.GET:
            term = request.GET.getlist('term')
            class_student = ClassRoomStudent.objects.get(
                student__admissionNumber=add_number)
            class_section = class_student.classRoom.classSection
            class_room = ClassRoom.objects.get(classSection=class_section)
            subject_x = []

            # get subjects list for a particular classroom
            exam_mapping = ExamMapping.objects.filter(classroom=class_room)
            for a in exam_mapping:
                if a.subject not in subject_x:
                    subject_x.append(a.subject)
            subject_x.sort()

            # Get UT and SA marks according to term 1 or term 2
            try:
                if 'term1' in term and 'term2' not in term:
                    marks = Marks.objects.filter(
                        examName__examName='UT-1', classroomStudent=class_student)
                    ut1_y = []
                    for subject in subject_x:
                        ut1_y.append(marks.get(subject=subject).marks)

                    sa_1_y = []
                    marks = Marks.objects.filter(
                        examName__examName='SEA-1', classroomStudent=class_student)
                    for subject in subject_x:
                        sa_1_y.append(marks.get(subject=subject).marks)

                    width = 0.25
                    subjects = subject_x
                    subject_x = np.arange(len(subject_x))
                    plt.clf()

                    plt.xticks(subject_x, subjects)
                    plt.bar(subject_x-width, ut1_y, color="#444444",
                            label="UT-1", width=width)
                    plt.bar(subject_x, sa_1_y, color="#008fd5",
                            label="SEA-1", width=width)
                    plt.legend()
                    plt.title("Marks of Term 1")
                    plt.xlabel("Subjects")
                    plt.ylabel("Marks")
                    plt.tight_layout()
                    # plt.show()
                    fig1 = plt.gcf()
                    buf1 = io.BytesIO()
                    fig1.savefig(buf1, format='png')
                    buf1.seek(0)
                    string = base64.b64encode(buf1.read())
                    uri = 'data:image/png;base64,' + urllib.parse.quote(string)
                    return render(request, 'marks/studentReport.html', {'image':uri})

                elif 'term2' in term and 'term1' not in term:
                    marks = Marks.objects.filter(
                        examName__examName='UT-2', classroomStudent=class_student)
                    ut2_y = []
                    for subject in subject_x:
                        ut2_y.append(marks.get(subject=subject).marks)

                    sa_2_y = []
                    marks = Marks.objects.filter(
                        examName__examName='SEA-2', classroomStudent=class_student)
                    for subject in subject_x:
                        sa_2_y.append(marks.get(subject=subject).marks)

                    width = 0.25
                    subjects = subject_x
                    subject_x = np.arange(len(subject_x))
                    plt.xticks(subject_x, subjects)
                    plt.clf()

                    plt.bar(subject_x-width, ut2_y, color="#444444",
                            label="UT-2", width=width)
                    plt.bar(subject_x, sa_2_y, color="#008fd5",
                            label="SEA-2", width=width)
                    plt.legend()
                    plt.title("Marks of Term 2")
                    plt.xlabel("Subjects")
                    plt.ylabel("Marks")
                    plt.tight_layout()
                    # plt.show()
                    fig2 = plt.gcf()
                    buf2 = io.BytesIO()
                    fig2.savefig(buf2, format='png')
                    buf2.seek(0)
                    string = base64.b64encode(buf2.read())
                    urii = 'data:image/png;base64,' + urllib.parse.quote(string)
                    return render(request, 'marks/studentReport.html', {'image':urii})

                else:
                    marks = Marks.objects.filter(
                        examName__examName='UT-1', classroomStudent=class_student)
                    ut1_y = []
                    for subject in subject_x:
                        ut1_y.append(marks.get(subject=subject).marks)

                    sa_1_y = []
                    marks = Marks.objects.filter(
                        examName__examName='SEA-1', classroomStudent=class_student)
                    for subject in subject_x:
                        sa_1_y.append(marks.get(subject=subject).marks)

                    marks = Marks.objects.filter(
                        examName__examName='UT-2', classroomStudent=class_student)
                    ut2_y = []
                    for subject in subject_x:
                        ut2_y.append(marks.get(subject=subject).marks)

                    sa_2_y = []
                    marks = Marks.objects.filter(
                        examName__examName='SEA-2', classroomStudent=class_student)
                    for subject in subject_x:
                        sa_2_y.append(marks.get(subject=subject).marks)

                    width = 0.18
                    subjects = subject_x
                    subject_x = np.arange(len(subject_x))
                    plt.clf()

                    plt.xticks(subject_x, subjects)

                    plt.bar(subject_x-width, ut1_y, color="#444444",
                            label="UT-1", width=width, align='center')
                    plt.bar(subject_x, sa_1_y, color="#008fd5",
                            label="SEA-1", width=width, align='center')
                    plt.bar(subject_x+width, ut2_y, color="#4d6c67",
                            label="UT-2", width=width, align='center')
                    plt.bar(subject_x + width+width, sa_2_y, color="#c7ea56",
                            label="SEA-2", width=width, align='center')
                    plt.legend()
                    plt.title("Marks of Term 1 & Term 2")
                    plt.xlabel("Subjects")
                    plt.ylabel("Marks")
                    plt.tight_layout()
                    # plt.show()
                    fig3 = plt.gcf()
                    buf3 = io.BytesIO()
                    fig3.savefig(buf3, format='png')
                    buf3.seek(0)
                    string = base64.b64encode(buf3.read())
                    uri = 'data:image/png;base64,' + urllib.parse.quote(string)
                    return render(request, 'marks/studentReport.html', {'image':uri})
            except:
                messages.error(
                    request, "Ensure that marks and subjects are entered properly for the student")
                redirect('reportStudent')
            # redirect('reportStudent')
            return render(request, 'marks/studentReport.html', {'image':uri})
    return render(request, 'marks/studentReport.html')

@login_required
def class_report_analysis(request):
    """
    Generate two graphs one for pass/fail and other for min/max/avg in classroom.
    Graph is generated for Half-Yearly and Annual Exam combined
    Input: Class/Section
    Output: Two graph, pass/fail pie chart & bar graph of min/max/avg
    """
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.user_type == "Teacher":
        emp_id = user_profile.emp_id
        employee = Employee.objects.get(empID=emp_id)
        teacher = Teacher.objects.get(employee=employee)
        class_section = teacher.classTeacher
        classrooms = ClassRoom.objects.filter(classSection=class_section)
    else:
        classrooms = ClassRoom.objects.all()
    if request.method == "GET":
        plt.style.use("fivethirtyeight")
        if "class_room" in request.GET:
            class_room = request.GET["class_room"]
            marks = Marks.objects.filter(
                classroomStudent__classRoom__classSection=class_room)
            # ut_marks = marks.filter(examName__examName='UT-1') | marks.filter(examName__examName='UT-2')
            sa_marks = marks.filter(
                examName__examName='Half-Yearly') | marks.filter(examName__examName='Annual')
            pass_students = 0
            fail_students = 0
            didnt_appear = 0
            for sa_mark in sa_marks:
                if sa_mark.marks >= 33:
                    pass_students += 1
                elif sa_mark.marks < 33:
                    fail_students += 1
                else:
                    didnt_appear += 1
            labels = ['Pass', 'Fail', "Didn't Appear"]
            slices = [pass_students, fail_students, didnt_appear]
            plt.clf()
            plt.pie(slices, labels=labels, startangle=90, autopct='%1.1f%%')
            plt.title(f"Report for Half-Yearly and Annual Exam")
            plt.tight_layout()
            plt.show()
            fig1 = plt.gcf()
            buf1 = io.BytesIO()
            fig1.savefig(buf1, format='png')
            buf1.seek(0)
            string = base64.b64encode(buf1.read())
            uri1 = 'data:image/png;base64,' + urllib.parse.quote(string)


            # max, min and abg bar graph
            class_room = ClassRoom.objects.get(classSection=class_room)
            subject_x = []
            exam_mapping = ExamMapping.objects.filter(classroom=class_room)

            # get subjects
            for a in exam_mapping:
                if a.subject not in subject_x:
                    subject_x.append(a.subject)
            subject_x.sort()
            # get min,max,avg for each subject and plot bar graph
            highest = []
            minimum = []
            average = []
            marks = marks.filter(
                examName__examName='Half-Yearly') | marks.filter(examName__examName='Annual')

            for sub in subject_x:
                _marks = marks.filter(subject=sub)
                highest_marks = 0
                total_marks = 0
                min_marks = 999
                count = len(_marks)
                for mark in _marks:
                    # count += 1
                    total_marks += mark.marks
                    if mark.marks > highest_marks:
                        highest_marks = mark.marks
                    if mark.marks < min_marks:
                        min_marks = mark.marks

                average.append(total_marks/count)
                highest.append(highest_marks)
                minimum.append(min_marks)

            width = 0.22
            subjects = subject_x
            subject_x = np.arange(len(subject_x))
            plt.clf()
            plt.xticks(subject_x, subjects)
            plt.bar(subject_x - width, highest, color="#444444",
                    label="Max Marks", width=width, align='center')
            plt.bar(subject_x, average, color="#008fd5",
                    label="Avg Marks", width=width, align='center')
            plt.bar(subject_x + width, minimum, color="#4d6c67",
                    label="Min Marks", width=width, align='center')
            plt.legend()
            plt.title("Max, Avg and Min Standing")
            plt.xlabel("Subjects")
            plt.ylabel("Marks")
            # plt.show()
            # redirect('reportClass')
            plt.tight_layout()
            fig1 = plt.gcf()
            buf1 = io.BytesIO()
            fig1.savefig(buf1, format='png')
            buf1.seek(0)
            string = base64.b64encode(buf1.read())
            uri2 = 'data:image/png;base64,' + urllib.parse.quote(string)
            return render(request, 'marks/classReport.html', {'image1':uri1, "class_rooms": classrooms,'image2':uri2})


    return render(request, 'marks/classReport.html', {"class_rooms": classrooms})

@login_required
def student_marks_filter(request):
    """
    Display and filter the marks according to exam name, exam type, subject
    """
    user_profile = UserProfile.objects.get(user=request.user)
    exam_types = ExamType.objects.all().values('examType').distinct()
    exam_names = Exam.objects.all()
    exam_mapping_subjects = ExamMapping.objects.all().values('subject').distinct()
    addmission_number = user_profile.addmission_number
    student = ClassRoomStudent.objects.get(student__admissionNumber=addmission_number)
    marks = Marks.objects.filter(classroomStudent=student)
    exam_name = request.GET.get("exam_name")
    exam_type = request.GET.get("exam_type")
    subject = request.GET.get("subject")
    if exam_name != '' and exam_name is not None:
        marks = Marks.objects.filter(examName__examName=(exam_name))
    if exam_type != '' and exam_type is not None:
        marks = Marks.objects.filter(examType__examType=(exam_type))
    if subject != '' and subject is not None:
        marks = Marks.objects.filter(subject=subject)

    context = {
        "exam_names":exam_names,
        "exam_types":exam_types,
        "exam_mapping_subjects":exam_mapping_subjects,
        "marks":marks
    }
    return render(request, "marks/studentMarksFilter.html", context)

def marks_sheet(request):
    if request.method == 'POST':
        if 'add_no' in request.POST:
            add_no = request.POST['add_no']
            class_rooms = request.POST['class_room']
            marks = Marks.objects.filter(classroomStudent__classRoom__classSection=class_rooms, classroomStudent__student__admissionNumber=add_no)
            if marks:
                messages.success(request, 'Markssheet.')
                return render(request, 'marks/searchmarksheet.html', {"class_room": ClassRoom.objects.all(), "students": marks})
                # return render(request, 'marks/marksheet.html')
            else:
                messages.error(request, 'No Record exist')
                return render(request, 'marks/searchmarksheet.html', {"class_room": ClassRoom.objects.all()})
    return render(request, 'marks/searchmarksheet.html', {"class_room": ClassRoom.objects.all()})

def submark( id, examName, examType, subjects):
    mark = []
    for subject in subjects:
        marks = Marks.objects.get(classroomStudent__student__admissionNumber=id, examName__examName = examName, exam__examType__examType=examType, exam__classsubject__subject__name=subject)
        mark.append(marks.marks)
    count = 0
    for m in mark:
        if m == None:
            count += 1
    if count == len(mark):
        return 0
    else:
        return mark


def marksheet(request, add_no):
    marks = Marks.objects.filter(classroomStudent__student__admissionNumber=add_no).order_by('exam__classsubject').distinct('exam__classsubject')
    subjects = []
    i=0
    for mark in marks:
        print(mark)
        subjects.append(mark.exam.classsubject.subject.name)
    i=0
    exam = []
    marks = Marks.objects.filter(classroomStudent__student__admissionNumber=add_no).order_by('examName__examName').distinct('examName__examName')
    for mark in marks:
        exam.append(mark.examName.examName)
    examCategory = {}
    for e in exam:
        marks = Marks.objects.filter(classroomStudent__student__admissionNumber=add_no, examName__examName=e).order_by('exam__examType__examType').distinct('exam__examType__examType')
        li= []
        for mark in marks:
            marksub = submark(add_no, e, mark.exam.examType.examType, subjects)
            if not marksub == 0:
                temp = mark.exam.examType.examType
                li.append({temp: marksub})
            print(li)
        if not len(li) == 0:
            examCategory.update({ e : li})
            print(examCategory)
    return render(request, 'marks/marksheet.html', {"student": marks, "stumark": examCategory, "subjects": subjects})


