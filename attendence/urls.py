"""
Urls for attendence app
"""

from django.urls import path
from . import views

urlpatterns = [
    path('student', views.student_attendence, name="attendenceStudent"),
    path('piechartStudent', views.student_pie_chart, name="piechartStudent"),
    path('Student-Report', views.student_total_report, name="StudentReport"),
    path('Employee-Report', views.employee_total_report, name="report"),
    path('piechartTeacher', views.teacher_pie_chart, name="piechartTeacher"),
    path('employee-attendence', views.teacher_attendence, name="attendenceEmployee"),
]
