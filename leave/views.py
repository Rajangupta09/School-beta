from django.shortcuts import render, redirect
from employeeform.models import Employee
from form.models import StudentInfo
from .models import StudentLeave, EmployeeLeave
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import UserProfile

# Create your views here.

@login_required
def employee_leave(request):
    emp_id1 = UserProfile.objects.filter(user=request.user).values_list('emp_id')
    if request.method == "POST":
        emp_id = request.POST.get("emp_id")
        description = request.POST.get("description")
        subject = request.POST.get("subject")
        date_to = request.POST.get("date_to")
        date_from = request.POST.get("date_from")
        date_to = date(*map(int, date_to.split('-')))
        date_from = date(*map(int, date_from.split('-')))
        upload = request.FILES['leave_file']
        print(upload.name)
        leave_obj=EmployeeLeave(employee=Employee.objects.get(
            empID=emp_id1[0][0]), description=description, subject=subject, date_from=date_from, date_to=date_to,leave_file = request.FILES.get('leave_file'))
        leave_obj.save()
        messages.info(request, 'Leave Request Submitted')
    return render(request, "leave/employee.html",{'emp_id':emp_id1[0][0]})

@login_required
def student_leave(request):
    admsn = UserProfile.objects.filter(user=request.user).values_list('addmission_number')
    if request.method == "POST":
        admissionNumber = request.POST.get("admissionNumber")
        description = request.POST.get("description")
        subject = request.POST.get("subject")
        date_to = request.POST.get("date_to")
        date_from = request.POST.get("date_from")
        date_to = date(*map(int, date_to.split('-')))
        date_from = date(*map(int, date_from.split('-')))
        upload = request.FILES['leave_file']
        print(upload.name)
        leave_obj = StudentLeave.objects.create(student=StudentInfo.objects.get(
            admissionNumber=admsn[0][0]), description=description, subject=subject, date_from=date_from, date_to=date_to ,leave_file = request.FILES.get('leave_file'))
        # leave_obj.leave_file = request.FILES.get('leave_file')
        leave_obj.save()
        messages.info(request, 'Leave Request Submitted')
    return render(request, "leave/student.html",{'admsn_no':admsn[0][0]})

@login_required
def view_student_leaves(request):
    leaves = StudentLeave.objects.filter(approved=False, rejected=False)
    count = StudentLeave.objects.filter(status='Submitted').count()
    if len(leaves) == 0:
        return render(request, "leave/studentLeaveRequest.html")
    else:
        return render(request, "leave/studentLeaveRequest.html", {"leaves": leaves,'count':count})

@login_required
def approve_leave(request, id):
    leave = StudentLeave.objects.get(id=id)
    leave.approved = True
    leave.status = "Approved"
    leave.save()
    leaves = StudentLeave.objects.filter(approved=False, rejected=False)
    count = StudentLeave.objects.filter(status='Submitted').count()
    if len(leaves) == 0:
        return render(request, "leave/studentLeaveRequest.html")
    else:
        return render(request, "leave/studentLeaveRequest.html", {"leaves": leaves,'count':count})

@login_required
def reject_leave(request, id):
    leave = StudentLeave.objects.get(id=id)
    leave.rejected = True
    leave.status = "Rejected"
    leave.save()
    count = StudentLeave.objects.filter(status='Submitted').count()
    leaves = StudentLeave.objects.filter(approved=False, rejected=False)
    if len(leaves) == 0:
        return render(request, "leave/studentLeaveRequest.html")
    else:
        return render(request, "leave/studentLeaveRequest.html", {"leaves": leaves,'count':count})

@login_required
def leave_history(request):
    admsn = UserProfile.objects.filter(user=request.user).values_list('addmission_number')
    history = StudentLeave.objects.filter(student=admsn[0][0]).order_by('-submit_date')
    count = StudentLeave.objects.filter(status='Submitted').count()
    return render(request,'leave/studentleavehistory.html',{'history':history,'count':count})

@login_required
def all_leave_history(request):
    leaves = StudentLeave.objects.all()
    count = StudentLeave.objects.filter(status='Submitted').count()
    if len(leaves) == 0:
        return render(request, "leave/all_leave_history.html")
    else:
        return render(request, "leave/all_leave_history.html", {"leaves": leaves,'count':count})

@login_required
def view_employee_leaves(request):
    leaves = EmployeeLeave.objects.filter(approved=False, rejected=False)
    count = EmployeeLeave.objects.filter(status='Submitted').count()
    if len(leaves) == 0:
        return render(request, "leave/employeeLeaveRequest.html")
    else:
        return render(request, "leave/employeeLeaveRequest.html", {"leaves": leaves,'count':count})

@login_required
def approve_employee_leave(request, id):
    leave = EmployeeLeave.objects.get(id=id)
    leave.approved = True
    leave.status = "Approved"
    leave.save()
    leaves = EmployeeLeave.objects.filter(approved=False, rejected=False)
    count = EmployeeLeave.objects.filter(status='Submitted').count()
    if len(leaves) == 0:
        return render(request, "leave/employeeLeaveRequest.html")
    else:
        return render(request, "leave/employeeLeaveRequest.html", {"leaves": leaves,'count':count})

@login_required
def reject_employee_leave(request, id):
    leave = EmployeeLeave.objects.get(id=id)
    leave.rejected = True
    leave.status = "Rejected"
    leave.save()
    leaves = EmployeeLeave.objects.filter(approved=False, rejected=False)
    count = EmployeeLeave.objects.filter(status='Submitted').count()
    if len(leaves) == 0:
        return render(request, "leave/employeeLeaveRequest.html")
    else:
        return render(request, "leave/employeeLeaveRequest.html", {"leaves": leaves,'count':count})

@login_required
def employee_leave_history(request):
    admsn = UserProfile.objects.filter(user=request.user).values_list('emp_id')
    history = EmployeeLeave.objects.filter(employee=admsn[0][0]).order_by('-submit_date')
    count = EmployeeLeave.objects.filter(status='Submitted').count()
    return render(request,'leave/employeeleavehistory.html',{'history':history,'count':count})

@login_required
def all_employee_leave_history(request):
    leaves = EmployeeLeave.objects.all()
    count = EmployeeLeave.objects.filter(status='Submitted').count()
    if len(leaves) == 0:
        return render(request, "leave/all_employee_leave_history.html")
    else:
        return render(request, "leave/all_employee_leave_history.html", {"leaves": leaves,'count':count})

@login_required
def employee_leave_sort(request):
    sort = request.GET.get('sort')
    count = EmployeeLeave.objects.filter(status='Submitted').count()
    if sort:
        leaves = EmployeeLeave.objects.filter(status=sort)
        if len(leaves) == 0:
            return render(request, "leave/all_employee_leave_history.html")
        else:
            return render(request, "leave/all_employee_leave_history.html", {"leaves": leaves,'count':count})
    else:
        date = request.GET.get('date')
        lev = EmployeeLeave.objects.filter(submit_date__date=date)
        if len(lev) == 0:
            return render(request, "leave/all_employee_leave_history.html")
        else:
            return render(request, "leave/all_employee_leave_history.html", {"leaves": lev,'count':count})

@login_required
def student_leave_sort(request):
    sort = request.GET.get('sort')
    if sort:
        leaves = StudentLeave.objects.filter(status=sort)
        if len(leaves) == 0:
            return render(request, "leave/all_leave_history.html")
        else:
            return render(request, "leave/all_leave_history.html", {"leaves": leaves})
    else:
        date = request.GET.get('date')
        lev = StudentLeave.objects.filter(submit_date__date=date)
        if len(lev) == 0:
            return render(request, "leave/all_leave_history.html")
        else:
            return render(request, "leave/all_leave_history.html", {"leaves": lev})
