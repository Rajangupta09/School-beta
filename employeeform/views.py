"""
  Handle employee registration part
"""
import csv, io
from django.http import HttpResponse
from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from classform.models import ClassRoom
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile
from .models import Employee, Teacher, EmployeeDocuments, PermanentAddress, CurrentAddress
import sys
import pprint
from cryptography.fernet import Fernet
@login_required
def form(request):
    if(Employee.objects.count() == 0 ):
        pk_ = 1
    else :
        pk_ = Employee.objects.last().pk+1
    """
    add new employee info to employee and teacher table and set media path of documents
    input: form values
    """
    if request.method == "POST":
        # Student Details
        emp_id = request.POST.get("empID")
        dob = request.POST["DOB"]
        join_date = request.POST["joinDate"]
        f_name = request.POST.get("firstname", "")
        l_name = request.POST.get("lastname", "")
        gender = request.POST.get("gender", "")
        email = request.POST.get("email", "")
        a_number = request.POST.get("a_number")
        phone_number = request.POST.get("phone_number")
        blood_group = request.POST.get("blood_group", "")
        father_name = request.POST.get("father_name", "")
        mother_name = request.POST.get("mother_name", "")
        experience = request.POST.get("experience", "")
        marital_status = request.POST.get("marital_status", "")
        partner_name = request.POST.get("partnerName", "")
        curr_perm = request.POST.get("customCheck1", "")
        current_add1 = request.POST.get("currentinputAddress")
        current_add2 = request.POST.get("currentinputAddress2")
        current_city = request.POST.get("inputCity", "")
        current_state = request.POST.get("inputState", "")
        current_zip = request.POST.get("inputZip")
        if curr_perm == "True":
            perm_add1 = request.POST.get("currentinputAddress")
            perm_add2 = request.POST.get("currentinputAddress2")
            perm_city = request.POST.get("inputCity")
            perm_state = request.POST.get("inputState")
            perm_zip = request.POST.get("inputZip")
        else:
            perm_add1 = request.POST.get("perminputAddress", "")
            perm_add2 = request.POST.get("perminputAddress2", "")
            perm_city = request.POST.get("perminputCity", "")
            perm_state = request.POST.get("perminputState", "")
            perm_zip = request.POST.get("perminputZip", "")
        emp_category = request.POST.get("empCategory", "")
        if dob:
            dob = date(*map(int, dob.split('-')))
        if join_date:
            join_date = date(*map(int, join_date.split('-')))
        if emp_category == "teacher":
            specialization = request.POST.get("specialization", "")
            designation = request.POST.get("designation", "")
            classTeacher = request.POST.get("classTeacher", "")
        try:
            employee = Employee.objects.create(empID=emp_id)
        except:
            messages.error(request, "Employee ID already assigned")
            return redirect('employeeForm')
        employee.firstName = f_name
        employee.lastName = l_name
        employee.partnerName = partner_name
        if len(l_name) != 0:
            full_name = f_name + " " + l_name
            employee.fullName = full_name
        else:
            full_name = f_name
            employee.fullName = full_name
        if dob:
            employee.dob = dob
        if join_date:
            employee.joiningDate = join_date
        employee.marital_status = marital_status
        employee.experience = experience
        if current_add2:
            employee.currentAddress = current_add1 + " " + current_add2 + ", " +current_city + ", " + current_state + " - " + current_zip
        else:
            employee.currentAddress = current_add1 + " " + ", " +current_city+ ", " + current_state +"-" + current_zip
        if perm_add2:
            employee.permanentAddress = perm_add1 + " " + perm_add2 + ", " +perm_city + ", " + perm_state + "-" +perm_zip
        else:
            employee.permanentAddress = perm_add1 + ", " +perm_city + ", " + perm_state + " - " + perm_zip
        employee.gender = gender
        employee.email = email
        employee.bloodGroup = blood_group
        if phone_number:
            employee.mobile_number = phone_number
        if a_number:
            employee.aadharNumber = a_number
        employee.father_name = father_name
        employee.mother_name = mother_name
        if emp_category == "other":
            employee.empCategory = request.POST.get("other", "")
        employee.empCategory = emp_category
        try:
            employee.save()
        except:
            messages.error(request, "Error! could not be recorded")
            return redirect('employeeForm')
        permanent = PermanentAddress.objects.create(employee=employee)
        permanent.Address = perm_add1 + perm_add2
        permanent.Address1 = perm_add1
        permanent.Address2 = perm_add2
        permanent.zipCode = perm_zip
        permanent.state = perm_state
        permanent.city = perm_city
        permanent.save()

        current = CurrentAddress.objects.create(employee=employee)
        current.Address1 = current_add1
        current.Address = current_add1 + current_add2
        current.Address2 = current_add2
        current.zipCode = current_zip
        current.city = current_city
        current.state = current_state
        current.save()

        if emp_category == "teacher":
            teacher = Teacher.objects.create(employee=employee)
            teacher.specialization = specialization
            teacher.designation = designation
            teacher.save()
            #create id and password for teacher
            if classTeacher:
                classroom = ClassRoom.objects.get(classSection=classTeacher)
                classroom.class_teacher_alloted = True
                classroom.save()
                teacher.classTeacher = classTeacher
                teacher.save()

        user = User.objects.create_user(emp_id, email, phone_number)
        user_profile = UserProfile.objects.create(user=user, fullName=full_name , emp_id=emp_id)
        user_profile.mobile_no = phone_number
        user_profile.user_type = emp_category
        user_profile.password = phone_number
        user_profile.save()
            # alert message when class has already a class teacher


        documents = EmployeeDocuments.objects.create(employee=employee)
        documents.IdProof = request.FILES.get("idproof")
        documents.photo = request.FILES.get("photgraph")
        documents.qualificationDoc = request.FILES.get("qualificationDoc")
        documents.addressProof = request.FILES.get("addressProof")
        documents.otherDoc = request.FILES.get("otherDoc")
        documents.save()
        messages.success(request, "Record successfully added")
        return print(request, employee.pk)
    class_rooms = ClassRoom.objects.filter(class_teacher_alloted=False)
    return render(request, 'employee/recordForm.html',{"class_rooms":class_rooms, "pk_":pk_})

@login_required
def update(request):
    """
    update employee info in employee and teacher table
    input: form values
    """
    if request.method == "POST":
        # Employee Details
        emp_id = request.POST.get("empID")
        employee = Employee.objects.get(empID=int(emp_id))
        current , created= CurrentAddress.objects.get_or_create(employee=employee)
        permanent, created= PermanentAddress.objects.get_or_create(employee=employee)
        dob = request.POST.get("DOB")
        join_date = request.POST.get("joinDate")
        if dob:
            dob = date(*map(int, dob.split('-')))
        if join_date:
            join_date = date(*map(int, join_date.split('-')))
        f_Name = request.POST.get("firstname", employee.firstName)
        l_Name = request.POST.get("lastname", employee.lastName)
        gender = request.POST.get("gender", employee.gender)
        email = request.POST.get("email", employee.email)
        a_number = request.POST.get("a_number", employee.aadharNumber)
        phone_number = request.POST.get("phone_number", employee.mobile_number)
        blood_group = request.POST.get("blood_group", employee.bloodGroup)
        father_name = request.POST.get("father_name", employee.father_name)
        mother_name = request.POST.get("mother_name", employee.mother_name)
        experience = request.POST.get("experience", employee.experience)
        marital_status = request.POST.get(
            "marital_status", employee.marital_status)
        partner_name = request.POST.get("partnerName", employee.partnerName)
        currentAdd1 = request.POST.get(
            "currentinputAddress", current.Address1)
        currentAdd2 = request.POST.get(
            "currentinputAddress2", current.Address2)
        currentCity = request.POST.get("inputCity", current.city)
        currentState = request.POST.get("inputState", current.state)
        currentZip = request.POST.get("inputZip", current.zipCode)
        permAdd1 = request.POST.get("perminputAddress", permanent.Address1)
        permAdd2 = request.POST.get(
            "perminputAddress2", permanent.Address2)
        permCity = request.POST.get("perminputCity", permanent.city)
        permState = request.POST.get("perminputState", permanent.state)
        permZip = request.POST.get("perminputZip", permanent.zipCode)
        emp_category = request.POST.get("empCategory", employee.empCategory)
        if emp_category == "teacher":
            teacher, created = Teacher.objects.get_or_create(employee=employee)
            specialization = request.POST.get(
                "specialization", teacher.specialization)
            designation = request.POST.get(
                "designation", teacher.designation)
            classTeacher = request.POST.get(
                "classTeacher", teacher.classTeacher)

        employee.firstName = f_Name
        employee.lastName = l_Name
        employee.partnerName = partner_name
        if l_Name:
            employee.fullName = f_Name + " " + l_Name
        else:
            employee.fullName = f_Name
        if dob:
            employee.dob = dob
        if join_date:
            employee.joiningDate = join_date
        employee.marital_status = marital_status
        employee.experience = experience
        if currentAdd2:
            employee.currentAddress = currentAdd1 + " " + currentAdd2 + ", " + currentCity + ", " + currentState + " - " + currentZip
        else:
            employee.currentAddress = currentAdd1 + ", " + currentCity + ", " + currentState + " - " + currentZip
        if permAdd2:
            employee.permanentAddress = permAdd1 + " " + permAdd2 + ", " + permCity + ", " + permState + " - " + permZip
        else:
            employee.permanentAddress = permAdd1 + ", " + permCity + ", " + permState + " - " + permZip
        employee.gender = gender
        employee.email = email
        employee.mobileNumber = phone_number
        employee.bloodGroup = blood_group
        employee.aadharNumber = a_number
        employee.father_name = father_name
        employee.mother_name = mother_name
        employee.empCategory = emp_category
        employee.save()

        current.Address1 = currentAdd1
        current.Address2 = currentAdd2
        current.zipCode = currentZip
        current.state = currentState
        current.city = currentCity
        current.save()

        permanent.Address1 = permAdd1
        permanent.Address2 = permAdd2
        permanent.zipCode = permZip
        permanent.state = permState
        permanent.city = permCity
        permanent.save()

        if emp_category == "teacher":
            teacher, created = Teacher.objects.get_or_create(employee=employee)
            teacher.specialization = specialization
            teacher.designation = designation
            teacher.classTeacher = classTeacher
            teacher.save()

        messages.info(request, "Record successfully added")
        return redirect('employeeForm')
    return render(request, 'employee/updateInfo.html')

@login_required
def update_with_data(request, emp_id):
    """
    update form with actual data already filled in for required employee
    input: empID of employee and form values
    """
    try:
        employee = Employee.objects.get(empID=emp_id)
        if employee.is_deleted == True:
            messages.error(request, 'Employee don\'t Exist')
            return redirect('updateEmpInfo')
        else:
            p_add = PermanentAddress.objects.filter(employee=employee).first()
            teacher = Teacher.objects.filter(employee=employee).first()
            c_add = CurrentAddress.objects.filter(employee=employee).first()
            dob_to_string = str(employee.dob)
            join_date_to_string = str(employee.joiningDate)
            return render(request, 'employee/updateInfo.html',
                        {"employee": employee, "pAdd": p_add, "cAdd": c_add, "dob": dob_to_string,
                        "joiningDate": join_date_to_string, "teacher": teacher})
    except:
        messages.error(request, 'Employee don\'t Exist')
        return redirect('updateEmpInfo')

@login_required
def view_with_data(request, emp_id):
    """
    update form with actual data already filled in for required employee
    input: empID of employee and form values
    """
    try:
        employee = Employee.objects.get(empID=emp_id)
        if employee.is_deleted == True:
            messages.error(request, 'Employee don\'t Exist')
            return redirect('empSearchPage')
        else:
            p_add = PermanentAddress.objects.filter(employee=employee).first()
            teacher = Teacher.objects.filter(employee=employee).first()
            c_add = CurrentAddress.objects.filter(employee=employee).first()
            dob_to_string = str(employee.dob)
            join_date_to_string = str(employee.joiningDate)
            return render(request, 'employee/view.html',
                        {"employee": employee, "pAdd": p_add, "cAdd": c_add, "dob": dob_to_string,
                        "joiningDate": join_date_to_string, "teacher": teacher})
    except:
        messages.error(request, 'Employee don\'t Exist')
        return redirect('empSearchPage')


@login_required
def print(request, emp_id):
    """
    print info for employee
    input: empID number of whose data needs to be printed
    output: prints pdf with employee details
    """
    employee = Employee.objects.get(empID=emp_id)
    if employee.is_deleted == True:
        messages.error(request, 'Employee don\'t Exist')
        return redirect('empSearchPage')
    else:
        p_add = PermanentAddress.objects.filter(employee=employee).first()
        c_add = CurrentAddress.objects.filter(employee=employee).first()
        if employee.empCategory != "teacher":
            return render(request, 'employee/printEmployeeData.html', {"employee": employee, "pAdd": p_add, "cAdd": c_add})
        teacher = Teacher.objects.filter(employee=employee).first()
        return render(request, 'employee/printTeacherData.html',
                    {"employee": employee, "pAdd": p_add, "cAdd": c_add, "teacher": teacher})

@login_required
def search(request):
    """
    search employees
    input: employee category, employee id and name
    output: list of employee matching search query"""
    if request.method == "GET":
        employee = Employee.objects.all()
        if "name" in request.GET:
            name = request.GET["name"]
            employee = employee.filter(fullName__icontains=name, is_deleted=False)
        if "category" in request.GET:
            category = request.GET["category"]
            employee = employee.filter(empCategory__icontains=category, is_deleted=False)
        if "empID" in request.GET:
            emp_id = request.GET["empID"]
            if emp_id:
                employee = employee.filter(empID=emp_id, is_deleted=False)
            if employee:
                return render(request, 'employee/emplSearchPage.html', {"employees": employee, "values":request.GET})
            else:
                messages.error(request, 'Cant find employee with entered detail')
                return redirect('empSearchPage')
    return render(request, 'employee/emplSearchPage.html')

@login_required
def get_teachers_credentials(request):
    deletedEmployee = Employee.objects.all().filter(is_deleted=True)
    user_profile = UserProfile.objects.all().exclude(user_type="Student")
    user_profile = user_profile.exclude(user_type="Admin")
    for deemp in deletedEmployee:
        user_profile = user_profile.exclude(emp_id=deemp.empID)
    employee = Employee.objects.all().filter(is_deleted=False)
    # to render the one time key
    file = open('key.key', 'rb')
    key = file.read() # The key will be type bytes
    file.close()
    f = Fernet(key)
    pp = pprint.PrettyPrinter(indent=4)
    x = user_profile.values_list('password')
    decrypt_list = []
    translation = {39: None}
    # decrypted_message = f.decrypt(encrypted)
    # print(decrypted_message)
    # print(x[0][0])
    # encrypted=x[0][0]
    # decrypted = f.decrypt(encrypted)
        # print(decrypted)
    # ecrypted_message =encryption_type.decrypt
    myList = zip(user_profile, employee)
    # if request.method == 'GET':
    #     passws = request.GET.get('passws')
    #     pp.pprint(bytes(passws))
    return render(request, 'employee/credentials.html', {"myList":myList})


def export_employee_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Employee-Data.csv"'
    writer = csv.writer(response)
    writer.writerow(['Employee ID', 'Full Name', 'Employee Category', 'Gender', 'Date of birth', 'Email', 'Moblie Number', 'Experience', 'Father Name', 'Mother Name', 'Partner Name', 'Joining Date', 'Marital Status', 'Aadhar Number', 'Blood Group', 'Current Address', 'Current City' ,'Current State', 'Current Pin Code', 'Permanent Address', 'Permanent City' ,'Permanent State', 'Permanent Pin Code' ])
    employee = Employee.objects.all().values_list('empID', 'fullName', 'empCategory', 'gender', 'dob', 'email', 'mobile_number', 'experience', 'father_name', 'mother_name', 'partnerName', 'joiningDate', 'marital_status','aadharNumber', 'bloodGroup')
    # permanent = PermanentAddress.objects.filter(employee=employee).values_list('Address', 'city', 'state', 'zipCode')
    for employ in employee:
        current = CurrentAddress.objects.get(employee=employ)
        permanent = PermanentAddress.objects.get(employee=employ)
        current = (current.Address, current.city, current.state, current.zipCode)
        permanent = (permanent.Address, permanent.city, permanent.state, permanent.zipCode)
        writer.writerow(employ + current + permanent)
    # for curr in current:
    #     writer.writerow(curr)
    return response

def sample_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Sample Employee Data.csv"'
    writer = csv.writer(response)
    writer.writerow(['Employee ID', 'Full Name', 'Employee Category', 'Gender', 'Date of birth', 'Email', 'Moblie Number', 'Experience', 'Father Name', 'Mother Name', 'Partner Name', 'Joining Date', 'Marital Status', 'Aadhar Number', 'Blood Group', 'Current Address', 'Current City' ,'Current State', 'Current Pin Code', 'Permanent Address', 'Permanent City' ,'Permanent State', 'Permanent Pin Code' ])

    return response

def import_excel_data(request):
    data=[]
    prompt = {
        'order': 'Order of the CSV should be Employee ID, Full Name, Employee Category, Gender, date of birth (Format: YYYY-MM-DD), Email, Mobile Number, Experience, Father Name, Mother Name, Partner Name, joiningDate, marital_status, Aadhar Number, Blood Group, Current Address, Current City, Current State, Current PinCode, Permanent Address, Permanent City, Permanent State, Permanent PinCode.'
        }
    if request.method == 'POST':
        try:
            csv_file = request.FILES['excel']
            if not csv_file.name.endswith('.csv'):
                messages.error(request,'This is not a csv file')
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)
            reader = csv.reader(io_string, delimiter=',', quotechar='|')
            for column in reader:
                fullName=column[1]
                Name = fullName.split()
                firstName = Name[0]
                try:
                    lastName = Name[1]
                except:
                    lastName = ''
                empCategory=column[2]
                gender=column[3]
                dob=column[4]
                email=column[5]
                mobile_number=column[6]

                experience=column[7]
                father_name=column[8]
                mother_name=column[9]
                partnerName=column[10]
                joiningDate=column[11]
                marital_status=column[12]

                aadharNumber=column[13]
                bloodGroup=column[14]
                currentAddress=column[15]
                currentCity=column[16]
                currentState=column[17]
                currentZip=column[18]
                cAdd=currentAddress + ' ' + currentCity + ' ' + currentState + ' - ' + currentZip
                permanentAddress=column[19]
                permanentCity=column[20]
                permanentState=column[21]
                permanentZip=column[22]
                pAdd=permanentAddress + ' ' + permanentCity + ' ' + permanentState + ' - ' + permanentZip
                id=Employee.objects.last().pk+1
                created = Employee.objects.create(empID=id,fullName=fullName,firstName=firstName, lastName=lastName,
                empCategory=empCategory,
                email=email,
                aadharNumber=aadharNumber,bloodGroup=bloodGroup,
                currentAddress=cAdd,
                permanentAddress=pAdd,
                dob=dob, experience=experience,
                father_name=father_name, mother_name=mother_name, partnerName=partnerName,
                gender=gender,
                joiningDate=joiningDate,
                marital_status=marital_status,
                mobile_number=mobile_number)
                permanent = PermanentAddress.objects.create(employee=created, Address=permanentAddress, city=permanentCity, state=permanentState, zipCode=permanentZip)
                current = CurrentAddress.objects.create(employee=created, Address=currentAddress, city=currentCity, state=currentState, zipCode=currentZip)
                if empCategory == 'teacher':
                    try:
                        teacher = Teacher.objects.create(employee=created, specialization=column[23], designation=column[24], classTeacher=column[25])
                    except:
                        messages.warning(request,'Teacher details are not Provided')
                temp = {
                    'id':id, 'name':fullName, 'gender':gender, 'dob': dob, 'email':email, 'category':empCategory,
                }
                data.append(temp)
            messages.success(request, 'Data Uploaded SuccessFully.')
            return render(request, 'employee/uploadExcelData.html', {'list':data})
        except:
            messages.error(request, 'Your File cannot be Uploaded please verify the Order!')
            redirect('/Import-Data')
    return render(request, 'employee/uploadExcelData.html', {'prompt':prompt})


def trash(request):
    employee = Employee.objects.all().filter(is_deleted=True)
    return render(request, 'employee/deletedEmployee.html', {"employees": employee})

def delete(request, emp_id):
    employee = Employee.objects.get(empID = emp_id)
    user = User.objects.get(username=emp_id)
    user_profile = UserProfile.objects.get(emp_id=emp_id)
    try:
        user_profile.is_active = False
        user.is_active = False
        employee.is_deleted = True;
        user.save()
        user_profile.save()
        employee.save()
        messages.success(request, 'Successfully Moved to Trash')
        return redirect('/empForm/search')
    except:
        messages.error(request, 'Profile couldnot be deleted.')
    return redirect("/empForm/search")

def restore(request, emp_id):
    employee = Employee.objects.get(empID = emp_id)
    user = User.objects.get(username=emp_id)
    user_profile = UserProfile.objects.get(emp_id=emp_id)
    try:
        user_profile.is_active = True
        user.is_active = True
        employee.is_deleted = False;
        user.save()
        user_profile.save()
        employee.save()
        messages.success(request, 'Restored Successfully')
        return redirect('/empForm/search')
    except:
        messages.error(request, 'Profile couldnot be Restored.')
    return redirect("/empForm/search")

def permanent_delete(request, emp_id):
    employee = Employee.objects.get(empID = emp_id)
    user = User.objects.get(username = emp_id)
    p_add = PermanentAddress.objects.filter(employee=employee)
    teacher = Teacher.objects.filter(employee=employee)
    c_add = CurrentAddress.objects.filter(employee=employee)
    user.delete()
    employee.delete()
    messages.success(request, 'deleted Successfully')
    return redirect('/empForm/search')

def deactivate(request, emp_id):
    user = User.objects.get(username=emp_id)
    user_profile = UserProfile.objects.get(emp_id=emp_id)
    try:
        user_profile.is_active = False
        user.is_active = False
        user.save()
        user_profile.save()
        messages.success(request, 'Profile successfully disabled.')
    except:
        messages.error(request, 'Profile couldnot be disabled.')
    return redirect("/empForm/empCredentials")

def activate(request, emp_id):
    employee = Employee.objects.get(empID = emp_id)
    user = User.objects.get(username=emp_id)
    user_profile = UserProfile.objects.get(emp_id=emp_id)
    try:
        if employee.is_deleted == True:
            messages.error(request, 'Profile is Temporaily Deleted couldnot be Deactivated.')
            return redirect("/empForm/empCredentials")
        else:
            user_profile.is_active = True
            user.is_active = True
            user.save()
            user_profile.save()
            messages.success(request, 'Profile successfully Activated.')
    except:
        messages.error(request, 'Profile couldnot be Activated.')
    return redirect("/empForm/empCredentials")
