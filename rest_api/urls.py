from django.urls import path, include
from rest_framework import routers
from .viewsets import *

router = routers.DefaultRouter()
router.register('employees/documents',
                EmployeeDocumentUploadViewSet, 'upload-document')
router.register('employees/currentaddress',
                EmployeeCurrentAddressViewSet, 'emp-currentaddress')
router.register('employees/permanentaddress',
                EmployeePermanentAddressViewSet, 'emp-permanentaddress')
router.register('employees/teacher/attendence', TeacherAttendenceViewset)
router.register('employees/teacher', EmployeeTeacherViewset, 'emp-teacher')
router.register('employees', EmployeeViewSet, 'employee')
router.register('students/documents', StudentDocumentsViewSet, 'students')
router.register('students/parent', StudentParentInfoViewset)
router.register('students/attendence', StudentAttendenceViewset)
router.register('students/route/attendence', StudentRouteAttendenceViewset)
router.register('students/route', StudentRouteViewSet)
router.register('students/notice', StudentNoticeViewset)
router.register('students/permanentaddress', StudentPermanentAddressViewSet)
router.register('students/currentaddress',
                StudentCurrentAddressViewSet, 'current-address-student')
router.register('students', StudentInfoViewSet, 'student-info')
router.register('classroom/student', ClassRoomStudentViewset)
router.register('classroom/notice', ClassNoticeViewset)
router.register('classroom', ClassRoomViewset)
router.register('reportcard', ReportCardViewset)
router.register('homework', HomeWorkViewset)
router.register('syllabus', SyllabusViewset)
router.register('exams/type', ExamTypeViewset)
router.register('exams/mapping', ExamMappingViewset)
router.register('exams', ExamViewset)
router.register('marks', MarksViewset)
router.register('additional_subject_mapping', AdditionalSubjectMappingViewset)
router.register('timetable', ClassRoomSubjectTeacherViewset)
router.register('fine', FineViewset)
router.register('fees/discount', FeeDiscountViewset)
router.register('fees/category', FeeCategoryViewset)
router.register('fees/class_section', ClassSectionFeesViewset)
router.register('fees/cycle', FeeCycleViewset)
router.register('fees', FeesViewset)
router.register('transport/vehicle', VehicleViewset)
router.register('transport/driver', DriverViewset)
router.register('transport/routes', RoutesViewset)
router.register('transport/route_detail', RouteDetailViewset)
router.register('visitors', VisitorViewset)
router.register('gallery/album', AlbumViewset)
router.register('gallery/photos', PhotoViewset)
router.register('gallery/videos', VideoViewset)
router.register('newsletter', NewsletterViewset)
router.register('schoolinfo', SchoolInfoViewset)
router.register('holiday', HolidayViewset)
router.register('toughts', ToughtsViewset)

urlpatterns = [
    path('', include(router.urls)),
]
