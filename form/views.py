"""
  Handle student registration part
"""
import csv
import io
from datetime import date
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from classform.models import ClassRoom, ClassRoomStudent
from transport.models import Routes, RouteDetail
from employeeform.models import Employee, Teacher
from accounts.models import UserProfile
from .models import StudentInfo, PermanentAddress, CurrentAddress, ParentInfo, Documents, StudentRoute
from openpyxl import load_workbook

from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def form(request):
    """
    add student info to student and media path for documents
    input: form values
    """
    if(StudentInfo.objects.count() == 0):
        pk_ = 1
    else:
        pk_ = StudentInfo.objects.last().pk+1
    if request.method == "POST":
        # Student Details
        s_dob = request.POST["sDOB"]
        if s_dob:
            s_dob = date(*map(int, s_dob.split('-')))
        attributes = request.POST.get("attributes", "")
        f_name = request.POST.get("firstname", "")
        l_name = request.POST.get("lastname", "")
        gender = request.POST.get("gender", "")
        class_section = request.POST.get("classsection", "")
        add_number = request.POST.get("addmissionnumber", "")
        phone_number = request.POST.get("phone_number", "")
        current_add1 = request.POST.get("currentinputAddress", "")
        current_add2 = request.POST.get("currentinputAddress2", "")
        current_city = request.POST.get("inputCity", "")
        current_state = request.POST.get("inputState", "")
        current_zip = request.POST.get("inputZip", "")
        curr_perm = request.POST.get("customCheck1", "")
        if curr_perm == "on":
            perm_add1 = request.POST.get("currentinputAddress", "")
            perm_add2 = request.POST.get("currentinputAddress2", "")
            perm_city = request.POST.get("inputCity", "")
            perm_state = request.POST.get("inputState", "")
            perm_zip = request.POST.get("inputZip", "")
        else:
            perm_add1 = request.POST.get("perminputAddress", "")
            perm_add2 = request.POST.get("perminputAddress2", "")
            perm_city = request.POST.get("perminputCity", "")
            perm_state = request.POST.get("perminputState", "")
            perm_zip = request.POST.get("perminputZip", "")
        religion = request.POST.get("religion", "")
        caste = request.POST.get("caste", "")
        try:
            tc_number = request.POST.get("tcnumber", "")
            anumber = request.POST.get("anumber", "")
            siblingid = request.POST.get("siblingid", "")
            siblingid0 = request.POST.get("siblingid0", "")
            siblingid1 = request.POST.get("siblingid1", "")
            siblingid2 = request.POST.get("siblingid2", "")
        except:
            tc_number = None
            anumber = None
            siblingid = None
            siblingid0 = None
            siblingid1 = None
            siblingid2 = None

        routeID = request.POST.get("route_id", None)
        stoppage_name = request.POST.get("stoppage_name", "")
        shift_id = request.POST.get("shifts", "")
        feeCategory = request.POST.get("feeCategory", "")
        prevschool_name = request.POST.get("prevschoolname", "")

        try:
            student_info = StudentInfo.objects.create(
                admissionNumber=add_number)
        except:
            messages.error(request, "Admission Number already assigned")
            return redirect("/studentForm/")
        if class_section:
            # class Section check
            try:
                class_room = ClassRoom.objects.get(classSection=class_section)
                student_info.classSection = class_section
                student_info.save()
                ClassRoomStudent.objects.create(
                    classRoom=class_room, student=student_info)
            except Exception as e:
                messages.error(request, f"{str(e)}Class Doesn't Exist")
                return redirect('recordForm')
        student_info.firstName = f_name
        student_info.lastName = l_name
        if l_name:
            full_name = f_name + " "+l_name
            student_info.fullName = full_name
        else:
            full_name = f_name
            student_info.fullName = full_name
        student_info.attributes = attributes
        if s_dob:
            student_info.dob = s_dob
        student_info.gender = gender
        if phone_number:
            student_info.mobileNumber = phone_number
        student_info.religion = religion
        student_info.caste = caste
        if tc_number:
            student_info.tcNumber = tc_number
        if anumber:
            student_info.aadharNumber = anumber
        if feeCategory:
            student_info.feeWaiverCategory = feeCategory
        if siblingid:
            student_info.siblingID = siblingid
        if siblingid0:
            student_info.siblingID0 = siblingid0
        if siblingid1:
            student_info.siblingID1 = siblingid1
        if siblingid2:
            student_info.siblingID2 = siblingid2
        if prevschool_name:
            student_info.prevschoolname = prevschool_name
        student_info.save()

        # create id and password for student
        user = User.objects.create_user(
            username=add_number, password=phone_number)
        user_profile = UserProfile.objects.create(
            user=user, fullName=full_name, addmission_number=add_number)
        user_profile.user_type = "Student"
        user_profile.password = phone_number
        user_profile.save()

        permanent = PermanentAddress.objects.create(student=student_info)
        permanent.Address = perm_add1 + perm_add2
        permanent.Address1 = perm_add1
        permanent.Address2 = perm_add2
        permanent.zipCode = perm_zip
        permanent.state = perm_state
        permanent.city = perm_city
        permanent.save()

        current = CurrentAddress.objects.create(student=student_info)
        current.Address1 = current_add1
        current.Address = current_add1 + current_add2
        current.Address2 = current_add2
        current.zipCode = current_zip
        current.city = current_city
        current.state = current_state
        current.save()
        # Parent Details
        father_name = request.POST.get("fathername")
        mother_name = request.POST.get("mothername")
        m_dob = request.POST.get("mDOB")
        f_dob = request.POST.get("fDOB")
        pphone_number = request.POST.get("pphone_number")
        alt_pphone_number = request.POST.get("alt_pphone_number")
        g_qual = request.POST.get("g_qual")
        pemail = request.POST.get("pemail")
        m_qual = request.POST.get("m_qual")
        m_occup = request.POST.get("m_occup")
        g_occup = request.POST.get("g_occup")
        if m_dob:
            mDOB = date(*map(int, m_dob.split('-')))
        if f_dob:
            fDOB = date(*map(int, f_dob.split('-')))

        parent_info = ParentInfo.objects.create(student=student_info)
        parent_info.fatherName = father_name
        parent_info.motherName = mother_name
        if f_dob:
            parent_info.Fatherdob = f_dob
        if m_dob:
            parent_info.Motherdob = m_dob
        if pphone_number:
            parent_info.MobileNumber = pphone_number
        if alt_pphone_number:
            parent_info.altMobileNumber = alt_pphone_number
        parent_info.gaurdianQual = g_qual
        parent_info.guardianOccup = g_occup
        parent_info.email = pemail
        parent_info.motherQual = m_qual
        parent_info.motherQual = m_occup
        parent_info.save()
        # Route details

        if routeID:
            try:
                routeID = int(routeID)
                route = Routes.objects.get(routeID=routeID)
                student_route = StudentRoute.objects.create(
                    student=student_info)
                student_route.route_stoppage = stoppage_name

                if(shift_id == 'both'):
                    student_route_2 = StudentRoute.objects.create(
                        student=student_info)
                    student_route_2.stoppage_name = stoppage_name
                    student_route.shift = route.afternoon_shift
                    student_route_2.shift = route.morning_shift
                    student_route.save()
                    student_route_2.save()
                else:
                    shift = RouteDetail.object.get(id=int(shift_id))
                    student_route.shift = shift
                    student_route.save()

            except Exception as e:
                print(e)

        documents = Documents.objects.create(student=student_info)
        documents.idProof = request.FILES.get("idproof")
        documents.photo = request.FILES.get("photgraph")
        documents.castCertificate = request.FILES.get("castcert")
        documents.domicile = request.FILES.get("domicile")
        documents.tc = request.FILES.get("tc")
        documents.characterCertificate = request.FILES.get("charcert")
        documents.save()
        messages.success(request, "Record successfully added")
        return printinfo(request, student_info.pk)
    class_sections = [x.classSection for x in ClassRoom.objects.all()]
    return render(request, 'form/recordForm.html', {"routes": Routes.objects.all(), "class_sections": class_sections, "pk_": pk_})


@login_required
def update(request):
    """
    update student info in student table
    input: form values
    """
    if request.method == "POST":
        # Student Details
        add_number = request.POST.get("admissionNumber")
        student_info = StudentInfo.objects.get(
            admissionNumber=int(add_number))
        permanent, created = PermanentAddress.objects.get_or_create(
            student=student_info)
        current, created = CurrentAddress.objects.get_or_create(
            student=student_info)
        sDOB = request.POST.get("sDOB")
        if sDOB:
            sDOB = date(*map(int, sDOB.split('-')))
        f_name = request.POST.get("firstname", student_info.firstName)
        l_name = request.POST.get("lastname", student_info.lastName)
        gender = request.POST.get("gender", student_info.gender)
        sDOB = request.POST.get("sDOB", student_info.dob)
        classSection = request.POST.get(
            "classsection", student_info.classSection)
        phone_number = request.POST.get(
            "phone_number", student_info.mobileNumber)
        current_add1 = request.POST.get(
            "currentinputAddress", current.Address1)
        current_add2 = request.POST.get(
            "currentinputAddress2", current.Address2)
        current_city = request.POST.get("inputCity", current.city)
        current_state = request.POST.get("inputState", current.state)
        current_zip = request.POST.get("inputZip", current.zipCode)
        perm_add1 = request.POST.get(
            "perminputAddress", permanent.Address1)
        perm_add2 = request.POST.get(
            "perminputAddress2", permanent.Address2)
        perm_city = request.POST.get("perminputCity", permanent.city)
        perm_state = request.POST.get("perminputState", permanent.state)
        perm_zip = request.POST.get("perminputZip", permanent.zipCode)
        religion = request.POST.get("religion", student_info.religion)
        caste = request.POST.get("caste", student_info.caste)
        tc_number = request.POST.get("tcnumber", student_info.tcNumber)
        a_number = request.POST.get("anumber", student_info.aadharNumber)
        fee_category = request.POST.get(
            "feeCategory", student_info.feeWaiverCategory)
        sibling_id = request.POST.get("siblingid", student_info.siblingID)
        prevschool_name = request.POST.get(
            "prevschoolname", student_info.prevschoolname)

        # store current and perm address
        permanent.Address1 = perm_add1
        permanent.Address2 = perm_add2
        permanent.city = perm_city
        permanent.zipCode = perm_zip
        permanent.state = perm_state
        permanent.save()

        current.Address1 = current_add1
        current.Address2 = current_add2
        current.city = current_city
        current.zipCode = current_zip
        current.state = current_state
        current.save()

        student_info.firstName = f_name
        student_info.lastName = l_name
        student_info.dob = sDOB
        student_info.classSection = classSection
        student_info.permanentAddress = perm_add1 + perm_add2
        student_info.gender = gender
        student_info.mobileNumber = phone_number
        if religion:
            student_info.religion = religion
        if caste:
            student_info.caste = caste
        if tc_number:
            student_info.tcNumber = tc_number
        student_info.aadharNumber = a_number
        if fee_category:
            student_info.feeWaiverCategory = fee_category
        if sibling_id:
            student_info.siblingID = sibling_id
        if prevschool_name:
            student_info.prevschoolname = prevschool_name
        student_info.save()
        # Parent Details
        father_name = request.POST.get("fathername")
        mother_name = request.POST.get("mothername")
        m_dob = request.POST.get("mDOB")
        f_dob = request.POST.get("fDOB")
        pphone_number = request.POST.get("pphone_number")
        alt_pphone_number = request.POST.get("alt_pphone_number")
        g_qual = request.POST.get("g_qual")
        pemail = request.POST.get("pemail")
        m_qual = request.POST.get("m_qual")
        m_occup = request.POST.get("m_occup")
        g_occup = request.POST.get("g_occup")
        if m_dob:
            mDOB = date(*map(int, m_dob.split('-')))
        if f_dob:
            fDOB = date(*map(int, f_dob.split('-')))

        parent_info = ParentInfo.objects.get_or_create(student=student_info)
        parent_info.fatherName = father_name
        parent_info.motherName = mother_name
        if f_dob:
            parent_info.Fatherdob = f_dob
        if m_dob:
            parent_info.Motherdob = m_dob
        if pphone_number:
            parent_info.MobileNumber = pphone_number
        if alt_pphone_number:
            parent_info.altMobileNumber = alt_pphone_number
        parent_info.gaurdianQual = g_qual
        parent_info.guardianOccup = g_occup
        parent_info.email = pemail
        parent_info.motherQual = m_qual
        parent_info.motherQual = m_occup
        parent_info.save()

        messages.success(request, 'Updated the details')
        return redirect('updateInfo')
    class_sections = [x.classSection for x in ClassRoom.objects.all()]
    return render(request, 'form/updateInfo.html', {'class_sections': class_sections})


@login_required
def update_with_data(request, admission_number):
    """
    update form with actual data already filled in for required student
    input: admission number of student and form values

    """
    try:
        student_info = StudentInfo.objects.get(
            admissionNumber=(admission_number))
        if student_info.is_deleted == True:
            messages.error(request, 'Student Dosen\'t exist')
            class_sections = [x.classSection for x in ClassRoom.objects.all()]
            return redirect('updateInfo')
        else:
            p_add = PermanentAddress.objects.filter(
                student=student_info).first()
            c_add = CurrentAddress.objects.filter(student=student_info).first()
            parent_info = ParentInfo.objects.filter(
                student=student_info).first()
            DOB_to_String = str(student_info.dob)
            class_sections = [x.classSection for x in ClassRoom.objects.all()]
            return render(request, 'form/updateInfo.html', {"student": student_info, "pAdd": p_add, "cAdd": c_add, "dob": DOB_to_String, "class_sections": class_sections, "parent": parent_info})
    except:
        messages.error(request, 'Student Dosen\'t exist')
        class_sections = [x.classSection for x in ClassRoom.objects.all()]
        return redirect('updateInfo')


def view_with_data(request, admission_number):
    """
    update form with actual data already filled in for required student
    input: admission number of student and form values

    """
    try:
        student_info = StudentInfo.objects.get(
            admissionNumber=(admission_number))
        parent_info = ParentInfo.objects.filter(student=student_info).first()
        p_add = PermanentAddress.objects.filter(student=student_info).first()
        c_add = CurrentAddress.objects.filter(student=student_info).first()
        DOB_to_String = str(student_info.dob)
        class_sections = [x.classSection for x in ClassRoom.objects.all()]
        return render(request, 'form/viewstudent.html',
                      {"student": student_info, "pAdd": p_add, "cAdd": c_add, "dob": DOB_to_String, "class_sections": class_sections, "parent": parent_info})
    except:
        messages.error(request, 'Student Dosen\'t exist')
        class_sections = [x.classSection for x in ClassRoom.objects.all()]
        return redirect('updateInfo')


@login_required
def update_by_search(request):
    a_num = request.GET['admission_number_search']
    return update_with_data(request, a_num)


@login_required
def printinfo(request, admission_number):
    """
    print info for student
    input: admission number of whose data needs to be printed
    output: prints pdf with student details
    """
    student_info = StudentInfo.objects.get(admissionNumber=(admission_number))
    p_add = PermanentAddress.objects.get(student=student_info)
    c_add = CurrentAddress.objects.get(student=student_info)
    parent = ParentInfo.objects.get(student=student_info)
    return render(request, 'form/printStudentData.html',
                  {"student": student_info, "pAdd": p_add, "parent": parent, "cAdd": c_add})


@login_required
def search(request):
    """
    search students
    input: father's name, admission number,class section and name
    output: list of students matching search query
    """
    class_sections = [x.classSection for x in ClassRoom.objects.all()]
    if request.method == "GET":
        students = StudentInfo.objects.all()
        if "f_name" in request.GET:
            f_name = request.GET["f_name"]
            students = students.filter(
                parent__fatherName__icontains=f_name, is_deleted=False)
        if "name" in request.GET:
            name = request.GET["name"]
            students = students.filter(
                fullName__icontains=name, is_deleted=False)
        if "classSection" in request.GET:
            class_section = request.GET["classSection"]
            students = students.filter(
                classSection__icontains=class_section, is_deleted=False)
        if "addNumber" in request.GET:
            add_no = request.GET["addNumber"]
            if add_no:
                students = students.filter(
                    admissionNumber=add_no, is_deleted=False)
            if students:
                return render(request, 'form/searchPage.html', {"students": students, "values": request.GET, "class_sections": class_sections})
            else:
                messages.error(
                    request, 'Cant find student with entered detail')
                return redirect('/studentForm/search')
    return render(request, 'form/searchPage.html', {"class_sections": class_sections})


def export_student_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Student-Data.csv"'
    writer = csv.writer(response)
    writer.writerow(['Admission Number', 'Full Name', 'Class', 'Gender', 'Date of Birth', 'Mobile Number', 'Aadhar Number', 'TC Number', 'Previous School Name', 'Caste', 'Religion', 'Sibling Admission Number', 'Fee Waiver Category', 'Father Name', 'Mother Name', 'Father DoB', 'Mother DoB',
                     'Mobile Number', 'Alternate Mobile Number', 'Email', 'Father Qualification', 'Father Occupation', 'Mother Qualification', 'Mother Occupation', 'Current Address', 'Current City', 'Current State', 'Current Pin Code', 'PermanentAddress', 'Permanent City', 'Permanent State', 'Permanent Pin Code'])
    students = StudentInfo.objects.all().values_list('admissionNumber', 'fullName', 'classSection', 'gender', 'dob',
                                                     'mobileNumber', 'aadharNumber', 'tcNumber', 'prevschoolname', 'caste', 'religion', 'siblingID', 'feeWaiverCategory')
    for student in students:
        current = CurrentAddress.objects.get(student=student)
        permanent = PermanentAddress.objects.get(student=student)
        parent = ParentInfo.objects.get(student=student)
        current = (current.Address, current.city,
                   current.state, current.zipCode)
        permanent = (permanent.Address, permanent.city,
                     permanent.state, permanent.zipCode)
        parent = (parent.fatherName, parent.motherName, parent.Fatherdob, parent.Motherdob, parent.MobileNumber,
                  parent.altMobileNumber, parent.email, parent.gaurdianQual, parent.guardianOccup, parent.motherQual, parent.motherOccup)
        writer.writerow(student + parent + current + permanent)
    return response


def sample_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Student-Data(Sample).csv"'
    writer = csv.writer(response)
    writer.writerow(['Admission Number', 'Full Name', 'Class', 'Gender', 'Date of Birth', 'Mobile Number', 'Aadhar Number', 'TC Number', 'Previous School Name', 'Caste', 'Religion', 'Sibling Admission Number', 'Fee Waiver Category', 'Father Name', 'Mother Name', 'Father DoB', 'Mother DoB',
                     'Mobile Number', 'Alternate Mobile Number', 'Email', 'Father Qualification', 'Father Occupation', 'Mother Qualification', 'Mother Occupation', 'Current Address', 'Current City', 'Current State', 'Current Pin Code', 'PermanentAddress', 'Permanent City', 'Permanent State', 'Permanent Pin Code'])
    return response


@login_required
def upload_excel_data(request):
    prompt = {
        'order': 'Order of the CSV should be Admission Number, Full Name, Class, Gender, Date of Birth, Mobile Number, Aadhar Number, TC Number, Previous School Name, Caste, Religion, Sibling Admission Number, Fee Waiver Category, Father Name, Mother Name, Father DoB, Mother DoB, Mobile Number, Alternate Mobile Number, Email, Father Qualification, Father Occupation, Mother Qualification, Mother Occupation, Current Address, Current City, Current State, Current Pin Code, PermanentAddress, Permanent City, Permanent State, Permanent Pin Code'
    }
    data = []
    if request.method == 'POST':
        try:
            csv_file = request.FILES['excel']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'This is not a csv file')
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)
            reader = csv.reader(io_string, delimiter=',', quotechar='|')
            for column in reader:
                fullName = column[1]
                Name = fullName.split(' ')
                firstName = Name[0]
                try:
                    lastName = Name[1]
                except:
                    lastName = ''
                classSection = column[2]
                gender = column[3]
                dob = column[4]
                mobile_number = column[5]
                aadharNumber = column[6]
                tcNumber = column[7]
                prevschoolname = column[8]
                caste = column[9]
                religion = column[10]
                siblingID = column[11]
                if siblingID == '':
                    siblingID = 0
                feeWaiverCategory = column[12]

                fatherName = column[13]
                motherName = column[14]
                Fatherdob = column[15]
                Motherdob = column[16]
                MobileNumber = column[17]
                altMobileNumber = column[18]
                if altMobileNumber == '':
                    altMobileNumber = 0
                email = column[19]
                gaurdianQual = column[20]
                guardianOccup = column[21]
                motherQual = column[22]
                motherOccup = column[23]

                currentAddress = column[24]
                currentCity = column[25]
                currentState = column[26]
                currentZip = column[27]
                permanentAddress = column[28]
                permanentCity = column[29]
                permanentState = column[30]
                permanentZip = column[31]
                id = StudentInfo.objects.last().pk+1
                created = StudentInfo.objects.create(admissionNumber=id, fullName=fullName, firstName=firstName, lastName=lastName,
                                                     classSection=classSection, religion=religion, caste=caste,
                                                     aadharNumber=aadharNumber, tcNumber=tcNumber, prevschoolname=prevschoolname,
                                                     dob=dob, gender=gender, feeWaiverCategory=feeWaiverCategory,
                                                     mobileNumber=mobile_number, siblingID=siblingID)
                parent = ParentInfo.objects.create(student=created, fatherName=fatherName, motherName=motherName, Fatherdob=Fatherdob, Motherdob=Motherdob, MobileNumber=MobileNumber,
                                                   altMobileNumber=altMobileNumber, gaurdianQual=gaurdianQual, guardianOccup=guardianOccup, email=email, motherQual=motherQual, motherOccup=motherOccup)
                permanent = PermanentAddress.objects.create(
                    student=created, Address=permanentAddress, city=permanentCity, state=permanentState, zipCode=permanentZip)
                current = CurrentAddress.objects.create(
                    student=created, Address=currentAddress, city=currentCity, state=currentState, zipCode=currentZip)
                temp = {
                    'id': id, 'name': fullName, 'gender': gender, 'dob': dob, 'fatherName': fatherName, 'class': classSection,
                }
                data.append(temp)
            messages.success(request, 'Data Uploaded SuccessFully.')
            return render(request, 'form/uploadExcelData.html', {'list': data})
        except:
            messages.error(
                request, 'Your File cannot be Uploaded please verify the Order!')
            redirect('/uploadExcel')
    return render(request, 'form/uploadExcelData.html', {'prompt': prompt})


@login_required
def get_students_list(request):
    teacher_profile = UserProfile.objects.get(user=request.user)
    emp_id = teacher_profile.emp_id
    employee = Employee.objects.get(empID=emp_id)
    teacher = Teacher.objects.get(employee=employee)
    class_section = teacher.classTeacher
    students = ClassRoomStudent.objects.filter(
        classRoom__classSection=class_section)
    return render(request, "form/studentList.html", {"class_room_students": students})


@login_required
def get_student_credentials(request):
    deletedStudent = StudentInfo.objects.all().filter(is_deleted=True)
    user_profile = UserProfile.objects.filter(user_type="Student")
    for deemp in deletedStudent:
        user_profile = user_profile.exclude(
            addmission_number=deemp.admissionNumber)
    students = ClassRoomStudent.objects.all()
    myList = zip(user_profile, students)
    return render(request, 'form/credentials.html', {"myList": myList})


@login_required
def trash(request):
    students = StudentInfo.objects.all().filter(is_deleted=True)
    return render(request, 'form/deletedstudent.html', {"students": students})


@login_required
def delete(request, admission_number):
    students = StudentInfo.objects.get(admissionNumber=(admission_number))
    user = User.objects.get(username=admission_number)
    user_profile = UserProfile.objects.get(
        addmission_number=(admission_number))
    try:
        user_profile.is_active = False
        user.is_active = False
        students.is_deleted = True
        user.save()
        user_profile.save()
        students.save()
        messages.success(request, 'Successfully Moved to Trash')
        return redirect('/studentForm/search')
    except:
        messages.error(request, 'Profile couldnot be Deleted.')
    return redirect("/studentForm/search")


@login_required
def restore(request, admission_number):
    students = StudentInfo.objects.get(admissionNumber=(admission_number))
    user = User.objects.get(username=admission_number)
    user_profile = UserProfile.objects.get(
        addmission_number=(admission_number))
    try:
        user_profile.is_active = True
        user.is_active = True
        students.is_deleted = False
        user.save()
        user_profile.save()
        students.save()
        messages.success(request, 'Successfully Restored')
        return redirect('/studentForm/search')
    except:
        messages.error(request, 'Profile couldnot be Restored.')
    return redirect("/studentForm/search")


def permanent_delete(request, admission_number):
    students = StudentInfo.objects.get(admissionNumber=(admission_number))
    user = User.objects.get(username=admission_number)
    p_add = PermanentAddress.objects.filter(student=students).first()
    c_add = CurrentAddress.objects.filter(student=students).first()
    user.delete()
    students.delete()
    messages.success(request, 'deleted Successfully')
    return redirect('/studentForm/Deleted_Student')


def deactivate(request, admission_number):
    user = User.objects.get(username=admission_number)
    user_profile = UserProfile.objects.get(
        addmission_number=(admission_number))
    try:
        user_profile.is_active = False
        user.is_active = False
        user.save()
        user_profile.save()
        messages.success(request, 'Profile successfully disabled.')
    except:
        messages.error(request, 'Profile couldnot be disabled.')
    return redirect("/studentForm/studentCredentials")


def activate(request, admission_number):
    students = StudentInfo.objects.get(admissionNumber=(admission_number))
    user = User.objects.get(username=admission_number)
    user_profile = UserProfile.objects.get(
        addmission_number=(admission_number))
    try:
        if students.is_deleted == True:
            messages.error(
                request, 'Profile is Temporaily Deleted couldnot be Deactivated.')
            return redirect("/studentForm/studentCredentials")
        else:
            user_profile.is_active = True
            user.is_active = True
            user.save()
            user_profile.save()
            messages.success(request, 'Profile successfully Activated.')
    except:
        messages.error(request, 'Profile couldnot be Activated.')
    return redirect("/studentForm/studentCredentials")
