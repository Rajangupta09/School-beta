"""
Admin panel for employee form
"""
from django.contrib import admin
from .models import PermanentAddress, CurrentAddress, Employee, Teacher, EmployeeDocuments
# Register your models here.
admin.site.register(Teacher)

class EmplooyeeAdmin(admin.ModelAdmin):
    list_display = ('empID', 'fullName', 'is_deleted', 'empCategory')
    list_filter = ('empCategory',)
    list_per_page = 25
    list_editable = ('is_deleted',)

admin.site.register(Employee, EmplooyeeAdmin)
admin.site.register(EmployeeDocuments)
admin.site.register(PermanentAddress)
admin.site.register(CurrentAddress)

