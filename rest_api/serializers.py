from rest_framework import serializers
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
# serializers for student class


class StudentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = form.models.StudentInfo
        fields = '__all__'


class StudentCurrentAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = form.models.CurrentAddress
        fields = '__all__'


class StudentPermanentAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = form.models.PermanentAddress
        fields = '__all__'


class StudentParentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = form.models.ParentInfo
        fields = '__all__'


class StudentDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = form.models.Documents
        fields = '__all__'


class StudentRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = form.models.StudentRoute
        fields = '__all__'

# serializers for employee class


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = employeeform.models.Employee
        fields = '__all__'


class EmployeeCurrentAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = employeeform.models.CurrentAddress
        fields = '__all__'


class EmployeePermanentAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = employeeform.models.PermanentAddress
        fields = '__all__'


class EmployeeDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = employeeform.models.EmployeeDocuments
        fields = '__all__'


class EmployeeTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = employeeform.models.Teacher
        fields = '__all__'


# serializers for classform
class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = classform.models.ClassRoom
        fields = '__all__'


class ClassRoomStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = classform.models.ClassRoomStudent
        fields = '__all__'


class ReportCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = classform.models.ReportCard
        fields = '__all__'


class StudentRouteAttendenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = classform.models.StudentRouteAttendence
        fields = '__all__'

# serializers for notice


class ClassNoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = notice.models.ClassNotice
        fields = '__all__'


class StudentNoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = notice.models.StudentNotice
        fields = '__all__'

# serializers for homework and Syllabus


class HomeWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = homework.models.HomeWork
        fields = '__all__'


class SyllabusSerializer(serializers.ModelSerializer):
    class Meta:
        model = homework.models.Syllabus
        fields = '__all__'

# serializers for attendence


class StudentAttendenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = attendence.models.StudentAttendence
        fields = '__all__'


class TeacherAttendenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = attendence.models.TeacherAttendence
        fields = '__all__'

# serializers for markssection


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = markssection.models.Exam
        fields = '__all__'


class ExamTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = markssection.models.ExamType
        fields = '__all__'


class ExamMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = markssection.models.ExamMapping
        fields = '__all__'


class MarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = markssection.models.Marks
        fields = '__all__'


class AdditionalSubjectMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = markssection.models.AdditionalSubjectMapping
        fields = '__all__'


# serializers for timetable
class ClassRoomSubjectTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = timetable.models.ClassRoomSubjectTeacher
        fields = '__all__'

# serializers for fee


class FineSerializer(serializers.ModelSerializer):
    class Meta:
        model = fees.models.Fine
        fields = '__all__'


class FeeDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = fees.models.FeeDiscount
        fields = '__all__'


class FeeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = fees.models.FeeCategory
        fields = '__all__'


class ClassSectionFeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = fees.models.ClassSectionFees
        fields = '__all__'


class FeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = fees.models.Fee
        fields = '__all__'


class FeeCycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = fees.models.FeeCycle
        fields = '__all__'

# serializers for transport


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = transport.models.Vehicle
        fields = '__all__'


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = transport.models.Driver
        fields = '__all__'


class RoutesSerializer(serializers.ModelSerializer):
    class Meta:
        model = transport.models.Routes
        fields = '__all__'


class RouteDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = transport.models.RouteDetail
        fields = '__all__'

# serializers for visitors


class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = visitors.models.Visitor
        fields = '__all__'

# serializers for gallery


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = gallery.models.Album
        fields = '__all__'


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = gallery.models.Photo
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = gallery.models.Video
        fields = '__all__'

# serializers for newsletter


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = newsletter.models.Newsletter
        fields = '__all__'


# serializers for schoolinfo
class SchoolInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = schoolinfo.models.SchoolInfo
        fields = '__all__'

# serializers for holiday


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = holiday.models.Holidays
        fields = '__all__'

# serializers for dailytought


class ToughtsSerializer(serializers.ModelSerializer):
    class Meta:
        model = dailythought.models.Thoughts
        fields = '__all__'
