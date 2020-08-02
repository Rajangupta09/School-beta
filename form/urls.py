"""
student form urls
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.form, name="recordForm"),
    path('update', views.update, name="updateInfo"),
    path('usearch', views.update_by_search, name="update_by_search"),
    path('Deleted_Student', views.trash, name="stutrash"),
    path('search', views.search, name="searchPage"),
    path('Student-Data', views.export_student_csv, name="studata"),
    path('Student-Data-sample', views.sample_csv, name="student-sample"),
    path('uploadExcel', views.upload_excel_data, name="uploadExcelData"),
    path('studentCredentials', views.get_student_credentials, name="studentCredentials"),
    path('update/<int:admission_number>/', views.update_with_data, name="updateInfoWithData"),
    path('view/<int:admission_number>/', views.view_with_data, name="viewInfoWithData"),
    path('print/<int:admission_number>/', views.printinfo, name="printStudentData"),
    path('studentList', views.get_students_list, name="studentList"),
    path('Delete/<int:admission_number>', views.delete, name="sdelete"),
    path('Restore/<int:admission_number>', views.restore, name="srestore"),
    path('Permanent_Delete/<int:admission_number>', views.permanent_delete, name="spermanentdelete"),
    path('Deactivate/<int:admission_number>', views.deactivate, name="sdeactivate"),
    path('activate/<int:admission_number>/', views.activate, name="sactivate"),
]
