from django.urls import path
from . import views

urlpatterns = [
    path('employeeLeave/', views.employee_leave, name="employeeLeave"),
    path('studentLeave/', views.student_leave, name="studentLeave"),
    path('viewStudentLeaves/', views.view_student_leaves, name="viewStudentLeaves"),
    path('approveLeave/<int:id>/', views.approve_leave, name="approveLeave"),
    path('rejectLeave/<int:id>/', views.reject_leave, name="rejectLeave"),
    path('leavehistory/', views.leave_history, name="leave_history"),
    path('allleavehistory/', views.all_leave_history, name="all_leave_history"),
    path('viewEmployeeLeaves/', views.view_employee_leaves, name="viewEmployeeLeaves"),
    path('approveEmployeeLeave/<int:id>/', views.approve_employee_leave, name="approveEmployeeLeave"),
    path('rejectEmployeeLeave/<int:id>/', views.reject_employee_leave, name="rejectEmployeeLeave"),
    path('Employeeleavehistory/', views.employee_leave_history, name="employee_leave_history"),
    path('allemployeeleavehistory/', views.all_employee_leave_history, name="all_employee_leave_history"),
    path('Employeeleavesort/', views.employee_leave_sort, name="employee_leave_sort"),
    path('Studentleavesort/', views.student_leave_sort, name="student_leave_sort"),

]