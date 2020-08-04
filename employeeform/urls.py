"""
employee form urls
"""
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.form, name="employeeForm"),
    path('update', views.update, name="updateEmpInfo"),
    path('search', views.search, name="empSearchPage"),
    path('Deleted_Employee', views.trash, name="emptrash"),
    path('empCredentials', views.get_teachers_credentials, name="empCredentials"),
    path('update/<int:emp_id>/', views.update_with_data, name="updateEmpData"),
    path('view/<int:emp_id>/', views.view_with_data, name="viewEmpData"),
    path('print/<int:emp_id>/', views.print, name="printEmpData"),
    path('Employee-Data', views.export_employee_csv, name="empdata"),
    path('Import-Data', views.import_excel_data, name='empimport'),
    path('samplecsv',views.sample_csv, name='sample'),
    path('Delete/<int:emp_id>', views.delete, name="delete"),
    path('Restore/<int:emp_id>', views.restore, name="restore"),
    path('Permanent_Delete/<int:emp_id>', views.permanent_delete, name="permanentdelete"),
    path('Deactivate/<int:emp_id>/', views.deactivate, name="deactivate"),
    path('activate/<int:emp_id>/', views.activate, name="activate"),
    path('new', views.EmployeeCreateView.as_view(), name="new"),
]
