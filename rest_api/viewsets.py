from rest_framework import viewsets, response
from rest_framework.decorators import action
from .serializers import *
from django.db.models import Q
import employeeform
import form
import classform
import notice
import homework
import attendence
import markssection
import timetable
import fees
import transport
import visitors
import gallery
import newsletter
import schoolinfo
import dailythought
import holiday


class StudentInfoViewSet(viewsets.ModelViewSet):
    queryset = form.models.StudentInfo.objects.all()
    serializer_class = StudentInfoSerializer


class StudentCurrentAddressViewSet(viewsets.ModelViewSet):
    queryset = form.models.CurrentAddress.objects.all()
    serializer_class = StudentCurrentAddressSerializer


class StudentPermanentAddressViewSet(viewsets.ModelViewSet):
    queryset = form.models.PermanentAddress.objects.all()
    serializer_class = StudentCurrentAddressSerializer


class StudentParentInfoViewset(viewsets.ModelViewSet):
    queryset = form.models.ParentInfo.objects.all()
    serializer_class = StudentParentInfoSerializer


class StudentDocumentsViewSet(viewsets.ModelViewSet):
    queryset = form.models.Documents.objects.all()
    serializer_class = StudentDocumentsSerializer


class StudentRouteViewSet(viewsets.ModelViewSet):
    queryset = form.models.StudentRoute.objects.all()
    serializer_class = StudentRouteSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = employeeform.models.Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeCurrentAddressViewSet(viewsets.ModelViewSet):
    queryset = employeeform.models.CurrentAddress.objects.all()
    serializer_class = EmployeeCurrentAddressSerializer


class EmployeePermanentAddressViewSet(viewsets.ModelViewSet):
    queryset = employeeform.models.PermanentAddress.objects.all()
    serializer_class = EmployeePermanentAddressSerializer


class EmployeeDocumentUploadViewSet(viewsets.ModelViewSet):
    queryset = employeeform.models.EmployeeDocuments.objects.all()
    serializer_class = EmployeeDocumentsSerializer


class EmployeeTeacherViewset(viewsets.ModelViewSet):
    queryset = employeeform.models.Teacher.objects.all()
    serializer_class = EmployeeTeacherSerializer


class ClassRoomViewset(viewsets.ModelViewSet):
    queryset = classform.models.ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer

    @action(methods=['GET'], url_path='get-students', detail=True)
    def get_students(self, request, pk=None):
        classroom_students = classform.models.ClassRoom.objects.get(
            pk=pk).students.all()
        students = [
            classroom_student.student for classroom_student in classroom_students]
        serializer = StudentInfoSerializer(students, many=True)
        return response.Response(serializer.data)


class ClassRoomStudentViewset(viewsets.ModelViewSet):
    queryset = classform.models.ClassRoomStudent.objects.all()
    serializer_class = ClassRoomStudentSerializer


class ReportCardViewset(viewsets.ModelViewSet):
    queryset = classform.models.ReportCard.objects.all()
    serializer_class = ReportCardSerializer


class StudentRouteAttendenceViewset(viewsets.ModelViewSet):
    queryset = classform.models.StudentRouteAttendence.objects.all()
    serializer_class = StudentRouteAttendenceSerializer


class ClassNoticeViewset(viewsets.ModelViewSet):
    queryset = notice.models.ClassNotice.objects.all()
    serializer_class = ClassNoticeSerializer


class StudentNoticeViewset(viewsets.ModelViewSet):
    queryset = notice.models.StudentNotice.objects.all()
    serializer_class = StudentNoticeSerializer


class HomeWorkViewset(viewsets.ModelViewSet):
    queryset = homework.models.HomeWork.objects.all()
    serializer_class = HomeWorkSerializer


class SyllabusViewset(viewsets.ModelViewSet):
    queryset = homework.models.Syllabus.objects.all()
    serializer_class = SyllabusSerializer


class StudentAttendenceViewset(viewsets.ModelViewSet):
    queryset = attendence.models.StudentAttendence.objects.all()
    serializer_class = StudentAttendenceSerializer


class TeacherAttendenceViewset(viewsets.ModelViewSet):
    queryset = attendence.models.TeacherAttendence.objects.all()
    serializer_class = TeacherAttendenceSerializer


class ExamViewset(viewsets.ModelViewSet):
    queryset = markssection.models.Exam.objects.all()
    serializer_class = ExamSerializer


class ExamTypeViewset(viewsets.ModelViewSet):
    queryset = markssection.models.ExamType.objects.all()
    serializer_class = ExamTypeSerializer


class ExamMappingViewset(viewsets.ModelViewSet):
    queryset = markssection.models.ExamMapping.objects.all()
    serializer_class = ExamMappingSerializer


class MarksViewset(viewsets.ModelViewSet):
    queryset = markssection.models.Marks.objects.all()
    serializer_class = MarksSerializer


class AdditionalSubjectMappingViewset(viewsets.ModelViewSet):
    queryset = markssection.models.AdditionalSubjectMapping.objects.all()
    serializer_class = AdditionalSubjectMappingSerializer


class ClassRoomSubjectTeacherViewset(viewsets.ModelViewSet):
    queryset = timetable.models.ClassRoomSubjectTeacher.objects.all()
    serializer_class = ClassRoomSubjectTeacherSerializer


class FineViewset(viewsets.ModelViewSet):
    queryset = fees.models.Fine.objects.all()
    serializer_class = FineSerializer


class FeeDiscountViewset(viewsets.ModelViewSet):
    queryset = fees.models.FeeDiscount.objects.all()
    serializer_class = FeeDiscountSerializer


class FeeCategoryViewset(viewsets.ModelViewSet):
    queryset = fees.models.FeeCategory.objects.all()
    serializer_class = FeeCategorySerializer


class ClassSectionFeesViewset(viewsets.ModelViewSet):
    queryset = fees.models.ClassSectionFees.objects.all()
    serializer_class = ClassSectionFeesSerializer


class FeesViewset(viewsets.ModelViewSet):
    queryset = fees.models.Fee.objects.all()
    serializer_class = FeesSerializer


class FeeCycleViewset(viewsets.ModelViewSet):
    queryset = fees.models.FeeCycle.objects.all()
    serializer_class = FeeCycleSerializer


class VehicleViewset(viewsets.ModelViewSet):
    queryset = transport.models.Vehicle.objects.all()
    serializer_class = VehicleSerializer


class DriverViewset(viewsets.ModelViewSet):
    queryset = transport.models.Driver.objects.all()
    serializer_class = DriverSerializer


class RoutesViewset(viewsets.ModelViewSet):
    queryset = transport.models.Routes.objects.all()
    serializer_class = RoutesSerializer

    @action(detail=True, methods=['GET'])
    def get_shifts(self, request, pk=None):
        route = transport.models.Routes.objects.get(routeID=pk)
        shifts = transport.models.RouteDetail.objects.filter(
            Q(route_code_1=route) |
            Q(route_code_2=route)
        )
        serializer = RouteDetailSerializer(shifts, many=True)
        return response.Response(serializer.data)


class RouteDetailViewset(viewsets.ModelViewSet):
    serializer_class = RouteDetailSerializer
    queryset = transport.models.RouteDetail.objects.all()


class VisitorViewset(viewsets.ModelViewSet):
    queryset = visitors.models.Visitor.objects.all()
    serializer_class = VisitorSerializer


class AlbumViewset(viewsets.ModelViewSet):
    queryset = gallery.models.Album.objects.all()
    serializer_class = AlbumSerializer


class PhotoViewset(viewsets.ModelViewSet):
    queryset = gallery.models.Photo.objects.all()
    serializer_class = PhotoSerializer


class VideoViewset(viewsets.ModelViewSet):
    queryset = gallery.models.Video.objects.all()
    serializer_class = VideoSerializer


class NewsletterViewset(viewsets.ModelViewSet):
    queryset = newsletter.models.Newsletter.objects.all()
    serializer_class = NewsletterSerializer


class SchoolInfoViewset(viewsets.ModelViewSet):
    queryset = schoolinfo.models.SchoolInfo.objects.all()
    serializer_class = SchoolInfoSerializer


class HolidayViewset(viewsets.ModelViewSet):
    queryset = holiday.models.Holidays.objects.all()
    serializer_class = HolidaySerializer


class ToughtsViewset(viewsets.ModelViewSet):
    queryset = dailythought.models.Thoughts.objects.all()
    serializer_class = ToughtsSerializer
