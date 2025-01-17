from django.contrib import admin
from .models import ExamType, Marks, Exam, ExamMapping, AdditionalSubjectMapping, Skill, StudentSkill
# Register your models here.
admin.site.register(ExamType)
admin.site.register(Exam)
admin.site.register(Skill)
admin.site.register(StudentSkill)


admin.site.register(ExamMapping)
admin.site.register(AdditionalSubjectMapping)

class MarksAdmin(admin.ModelAdmin):
    list_filter =('examName',)
    # list_display = ('marks',)

admin.site.register(Marks, MarksAdmin)