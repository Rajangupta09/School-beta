from django.shortcuts import render, HttpResponse, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from xhtml2pdf import pisa
from django_xhtml2pdf.views import PdfMixin
import xlwt
from io import BytesIO
from django.template import Context
from .models import Vehicle, Routes, Driver, RouteDetail
from form.models import StudentRoute, StudentInfo
from accounts.models import UserProfile
from datetime import date
from django.contrib import messages
from employeeform.models import Employee
from .admin import VehicleList
from django.template.loader import get_template
from classform.models import StudentRouteAttendence, ClassRoomStudent
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic as generic_views
from .forms import *
from classform.forms import StudentRouteAttendenceForm
from django.http import Http404, HttpResponseRedirect
from django.forms import inlineformset_factory
from django.db.models import Q, Count
import calendar

# Create your views here.


@login_required
def vehicle_register(request):
    """
    Register new vehicle
    """
    if request.method == "POST":
        vehicle_number = request.POST.get("vehicleNumber")
        device_id = request.POST.get("deviceID")
        no_of_seat = request.POST.get("seats")
        maximum_allowed = request.POST.get("maximum")
        vehicle_type = request.POST.get("vehicleType")
        contact_person = request.POST.get("contactPerson")
        insurance_company = request.POST.get("insuranceCompany")
        insurance_date = request.POST.get("insuranceDate")
        insurance_date = date(*map(int, insurance_date.split('-')))
        pollution_cert_exp_date = request.POST.get("pollutionCertDate")
        pollution_cert_exp_date = date(
            *map(int, pollution_cert_exp_date.split('-')))
        permit_valid_date = request.POST.get("permitValidDate")
        permit_valid_date = date(*map(int, permit_valid_date.split('-')))
        service_date = request.POST.get("serviceDueDate")
        service_date = date(*map(int, service_date.split('-')))
        service_id = request.POST.get("serviceID")
        fitness_service_date = request.POST.get("fitnessServiceDate")
        fitness_service_date = date(*map(int, fitness_service_date.split('-')))
        Vehicle.objects.create(vehicle_no=vehicle_number, device_id=device_id, service_id=service_id, no_of_seat=no_of_seat, maximum_allowed=maximum_allowed, vehicle_type=vehicle_type, contact_person=contact_person,
                               insurance_company=insurance_company, permit_valid_date=permit_valid_date, insurance_date=insurance_date, pollution_cert_exp_date=pollution_cert_exp_date, fitness_service_date=fitness_service_date, service_date=service_date)
    return render(request, 'transport/vehicleRegister.html')


class DriverList(generic_views.ListView, LoginRequiredMixin):
    queryset = Employee.objects.filter(empCategory='driver')
    template_name = 'transport/driverList.html'


class DriverUpdate(generic_views.FormView, LoginRequiredMixin):

    """
    Using class based view for update driver
    data instead of function based view below
    """
    template_name = 'transport/driverRegister.html'
    form_class = DriverUpdateForm

    def get_success_url(self):
        return self.request.path

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        employee = get_object_or_404(Employee, empID=self.kwargs.get('empID'))
        try:
            driver = Driver.objects.get(employee=employee) or None
        except Driver.DoesNotExist:
            driver = None
        kwargs['instance'] = driver
        kwargs['employeeInstance'] = employee
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['empID'] = self.kwargs.get('empID')
        return context

    def create_success_message(self):
        messages.add_message(
            self.request,
            messages.INFO,
            'Sucessfully updated driver info'
        )

    def form_valid(self, form):
        if form.employeeForm.is_valid():
            form.employeeForm.save()
        form.save()
        self.create_success_message()
        return super().form_valid(form)


class RouteListView(generic_views.ListView, LoginRequiredMixin):
    template_name = "transport/routeList.html"
    queryset = Routes.objects.filter(Q(archived=False) | Q(archived=None))


class RouteRegisterView(generic_views.CreateView, LoginRequiredMixin):
    template_name = "transport/routeRegister.html"
    form_class = RouteForm
    success_url = reverse_lazy('routeList')

    def get_success_url(self):
        self.create_success_message()
        return super().get_success_url()

    def create_success_message(self):
        messages.add_message(
            self.request,
            messages.INFO,
            'Route created sucessfully'
        )


class RouteUpdateView(generic_views.UpdateView):
    template_name = 'transport/routeUpdate.html'
    form_class = RouteUpdateForm

    def get_success_url(self):
        self.create_success_message()
        return self.request.path

    def create_success_message(self):
        messages.add_message(
            self.request,
            messages.INFO,
            'Route updated sucessfully'
        )

    def get_object(self, *args, **kwargs):
        route_id = self.kwargs.get('routeID')
        route = get_object_or_404(Routes, routeID=route_id)
        return route

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shifts'] = RouteDetail.objects.filter(
            Q(route_code_1=self.object) |
            Q(route_code_2=self.object)
        )
        return context


class ShiftUpdateView(generic_views.UpdateView, LoginRequiredMixin):
    template_name = "transport/shiftUpdate.html"
    form_class = RouteDetailUpdateForm

    def create_success_message(self):
        messages.add_message(
            self.request,
            messages.INFO,
            'Shift updated sucessfully'
        )

    def get_success_url(self):
        self.create_success_message()
        return self.request.path

    def get_object(self, *args, **kwargs):
        route_detail_id = self.kwargs.get('detailID')
        route_detail = get_object_or_404(RouteDetail, id=route_detail_id)
        return route_detail

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = RouteDetail.objects.get(id=self.kwargs.get('detailID'))
        context['route'] = instance.route_code_1 or instance.route_code_2
        return context


class RouteDeleteView(generic_views.DeleteView):
    success_url = reverse_lazy('routeList')
    template_name = 'transport/deleteRoute.html'

    def get_object(self, queryset=None):
        routeID = self.kwargs.get('routeID')
        return Routes.objects.get(routeID=routeID)


class ShiftDeleteView(generic_views.DeleteView):
    template_name = 'transport/deleteShift.html'
    success_url = reverse_lazy('routeList')

    def get_object(self, queryset=None):
        detailID = self.kwargs.get('detailID')
        return RouteDetail.objects.get(id=detailID)

    def delete(self, *args, **kwargs):
        shift_object = self.get_object()
        route = shift_object.route_code_1 or shift_object.route_code_2
        shifts = RouteDetail.objects.filter(
            Q(route_code_1=route) |
            Q(route_code_2=route)
        ).count()

        if shifts > 1:
            route.shift_time = Routes.Shift.AFTERNOON if shift_object.route_code_1 else Routes.Shift.MORNING
            route.save()
            return super().delete(*args, **kwargs)
        else:
            route.delete()
            return redirect(reverse_lazy('routeList'))


@login_required
def route_archive_view(request, routeID):
    route = get_object_or_404(Routes, routeID=routeID)

    route.archived = True
    reverse_url = request.GET.get('next', 'routeList')
    route.save()
    if hasattr(route, 'morning_shift'):
        route.morning_shift.archived = True

    if hasattr(route, 'afternoon_shift'):
        route.afternoon_shift.archived = True

    return redirect(reverse_lazy(reverse_url))


@login_required
def shift_archive_view(request, routeID, detailID):
    routeDetail = get_object_or_404(RouteDetail, id=detailID)

    reverse_url = request.GET.get('next', 'routeList')
    routeDetail.archived = True
    routeDetail.save()
    return redirect(reverse_lazy(reverse_url))


@login_required
def vehicle_list(request):
    """
    Render all registered vehicle list
    """
    return render(request, 'transport/vehicleList.html', {"vehicles": Vehicle.objects.all()})


@login_required
def vehicle_list_excel(request):
    """
    Export vehicle list to excel sheet
    """
    dataset = VehicleList().export()
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename="vehicle-list.xlsx"'
    response.write(dataset.xlsx)
    return response


@login_required
def vehicle_list_pdf(request):
    """
    Export vehicle list to pdf
    """
    template_path = 'transport/vehicleListPdf.html'
    context = {"vehicles": Vehicle.objects.all()}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="vehicle-list.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render((context))

    # create a pdf
    pisaStatus = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisaStatus.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


class MarkAttendenceFilter(generic_views.TemplateView, LoginRequiredMixin):
    template_name = 'transport/markAttendenceFilter.html'

    def post(self, request, *args, **kwargs):
        shift_id = request.POST.get("shifts")
        next_ = request.GET.get('next')
        if not shift_id:
            messages.add_message(
                request,
                level=messages.WARNING,
                message="Please select a route"
            )
            return redirect(next_) if next_ else redirect(request.path)
        student_routes = StudentRoute.objects.filter(shift__id=shift_id)
        return redirect(reverse_lazy('markRouteAttendence', kwargs={'route_detail_id': shift_id}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['routes'] = Routes.objects.all()
        return context


class MarkRouteAttendence(generic_views.FormView, LoginRequiredMixin):
    template_name = 'transport/markAttendence.html'

    """
    form view implicitly checks for form.is_valid() and since
    our form is a list form form we have to extend list to include
    is_vaid methos
    """
    class FormList(list):
        def is_valid(self, *args, **kwargs):
            return True

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.INFO,
            'Sucessfully updated attendence'
        )
        return HttpResponseRedirect(self.request.path)

    def get_queryset(self):
        route_detail_id = self.kwargs.get('route_detail_id')
        return StudentRoute.objects.filter(shift__id=route_detail_id)

    def form_valid(self, form):
        for formset in form:
            if formset.is_valid():
                for form in formset:
                    if form.is_valid():
                        form.save()
            else:
                raise forms.ValidationError(formset.errors)

        return self.get_success_url()

    def get_form(self):
        queryset = self.get_queryset()
        formsets = MarkRouteAttendence.FormList()
        student_route_attendence_formset = inlineformset_factory(
            StudentRoute,
            StudentRouteAttendence,
            formset=StudentRouteAttendenceFormSet,
            form=StudentRouteAttendenceForm,
            extra=0,
            min_num=1,
            max_num=1,
            can_delete=False
        )
        for student_route in queryset:
            formsets.append(
                student_route_attendence_formset(
                    self.request.POST or None,
                    self.request.FILES or None,
                    instance=student_route,
                    prefix=f"student_route_{student_route.id}"
                )
            )

        return formsets

    def get_route_detail(self):
        route_detail_id = self.kwargs.get('route_detail_id')
        route_detail = RouteDetail.objects.get(id=route_detail_id)
        route = route_detail.route_code_1 or route_detail.route_code_2
        shift = Routes.Shift.MORNING if route_detail.route_code_1 else Routes.Shift.AFTERNOON
        return route.route_code, shift

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["routes"] = Routes.objects.all()
        context['route_code'], context['shift'] = self.get_route_detail()
        return context


class RouteAttendenceListFilter(generic_views.TemplateView, LoginRequiredMixin):
    template_name = 'transport/routeAttendenceListFilter.html'

    def post(self, request, *args, **kwargs):
        routeID = request.POST.get('routeID')
        student_id = request.POST.get('student_id')
        month = request.POST.get('month')
        next_ = request.GET.get('next', None)

        error = False

        if routeID and student_id:
            messages.add_message(
                request,
                level=messages.WARNING,
                message="Only one of route code and student can be chosen at a time"
            )
            error = True

        if not routeID and not student_id:
            messages.add_message(
                request,
                level=messages.WARNING,
                message="At least one of route code and student must be chosen"
            )
            error = True

        if month == '':
            messages.add_message(
                request,
                level=messages.WARNING,
                message="Month must be specified"
            )
            error = True

        if error:
            return redirect(next_) if next_ else redirect(request.path)

        _filter = 'student' if student_id else 'route'
        filter_id = student_id if _filter == 'student' else routeID
        kwargs = {'filter': _filter, 'filter_id': filter_id, 'month': month}
        return redirect(reverse_lazy('routeAttendenceList', kwargs=kwargs))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['routes'] = Routes.objects.all()
        context['students'] = StudentRoute.objects.all()
        return context


class RouteAttendenceList(generic_views.ListView, LoginRequiredMixin):
    template_name = 'transport/routeAttendenceList.html'

    def aggregate(self, queryset, routeID):
        '''
        aggregates all the attendence object in queryset based on student and
        stores their attendence info (no. of presents, no.of absents etc) in one pass.

        didn't know do this by standard aggregation methods 
        so an ugly workaround
        '''

        aggregated_list = []
        current_attendence_obj = None
        current_student_id = None

        applicable_shifts = Routes.objects.get(routeID=routeID).shift_time

        """ 
        this is aggregated status of a student over entire month
        the name of aggregated status and actual daily attendence status
        are same for easy lookup using getattr and setattr
        """
        aggregated_status = ['present', 'absent', 'late', 'leave']

        for attendence in queryset:
            """
            compares new attendence object to prev attendence object (the ids of student)

            if same => prev attendence object and new attendence object belong to same student
                        and we have to update aggregated status of prev object not adding this
                        object to list

            else    => attendence obj if for new student thus we need to append this new 
                        attendence object to aggregated list and initailize aggregated status
                        for this student
            """

            new_student_id = attendence.student_route.student.admissionNumber
            if current_student_id == None or current_student_id != new_student_id:
                aggregated_list.append(attendence)
                current_student_id = new_student_id
                current_attendence_obj = attendence

                """
                stores status for this student on day basis namely what was the status
                of this sutdent on the day attendence was taken
                """
                shift = Routes.Shift.MORNING if attendence.student_route.shift.route_code_1 else Routes.Shift.AFTERNOON

                """  
                getting shift status based on various conditins
                N/m stands for not yet marked
                N/a stands for not applicable (shift is not available)
                """
                if shift == Routes.Shift.MORNING:
                    status_morning = attendence.status
                    if applicable_shifts != Routes.Shift.BOTH:
                        status_afternoon = 'N/a'
                    elif status_morning == 'holiday':
                        status_afternoon = 'holiday'
                    else:
                        status_afternoon = 'N/m'
                elif shift == Routes.Shift.AFTERNOON:
                    status_afternoon = attendence.status
                    if applicable_shifts != Routes.Shift.BOTH:
                        status_morning = 'N/a'
                    elif status_afternoon == 'holiday':
                        status_morning = 'holiday'
                    else:
                        status_morning = 'N/m'

                current_attendence_obj.day_status = {
                    attendence.date.day: {
                        'morning': status_morning,
                        'afternoon': status_afternoon
                    }
                }

                """
                initialized aggreagted status and similtaneously records
                the status of this day. since name of aggregated status variable 
                and actual status is same setattr can be used in this way
                """
                for status in aggregated_status:
                    if current_attendence_obj.status == status:
                        setattr(current_attendence_obj, status, 1)
                    else:
                        setattr(current_attendence_obj, status, 0)

            else:
                count = getattr(current_attendence_obj, attendence.status)
                setattr(current_attendence_obj, attendence.status, count+1)
                shift = 'morning' if attendence.student_route.shift.route_code_1 else 'afternoon'

                if shift == Routes.Shift.MORNING:
                    status_morning = attendence.status
                    if applicable_shifts != Routes.Shift.BOTH:
                        status_afternoon = 'N/a'
                    elif status_morning == 'holiday':
                        status_afternoon = 'holiday'
                    else:
                        if current_attendence_obj.day_status.get(attendence.date.day) and current_attendence_obj.day_status.get(attendence.date.day).get('afternoon'):
                            status_afternoon = current_attendence_obj.day_status.get(
                                attendence.date.day).get('afternoon')
                        else:
                            status_afternoon = 'N/m'
                elif shift == Routes.Shift.AFTERNOON:
                    status_afternoon = attendence.status
                    if applicable_shifts != Routes.Shift.BOTH:
                        status_morning = 'N/a'
                    elif status_afternoon == 'holiday':
                        status_morning = 'holiday'
                    else:
                        if current_attendence_obj.day_status.get(attendence.date.day) and current_attendence_obj.day_status.get(attendence.date.day).get('morning'):
                            status_morning = current_attendence_obj.day_status.get(
                                attendence.date.day).get('morning')
                        else:
                            status_morning = 'N/m'

                if not current_attendence_obj.day_status.get(attendence.date.day):
                    current_attendence_obj.day_status[attendence.date.day] = {}

                current_attendence_obj.day_status[attendence.date.day] = {
                    'morning': status_morning,
                    'afternoon': status_afternoon
                }

        return aggregated_list

    def get_queryset(self):
        month = self.kwargs.get('month')
        year, month = list(map(int, month.split('-')))
        filter_id = self.kwargs.get('filter_id')
        filter_type = self.kwargs.get('filter')

        """
        get student_route_attendence for selected month of both shifts
        morning and afternoon
        """

        if filter_type == 'route':
            student_route_attendence = StudentRouteAttendence.objects.filter(
                (
                    Q(student_route__shift__route_code_1=filter_id) |
                    Q(student_route__shift__route_code_2=filter_id)
                ) &
                Q(date__month=month) &
                Q(date__year=year)
            ).order_by('student_route__student__admissionNumber', 'date')
            routeID = filter_id

        else:
            student_route_attendence = StudentRouteAttendence.objects.filter(
                Q(student_route__student__admissionNumber=filter_id) &
                Q(date__month=month) &
                Q(date__year=year)
            ).order_by('student_route__student__admissionNumber', 'date')

            route = student_route_attendence[0].student_route.shift.route_code_1 or student_route_attendence[0].student_route.shift.route_code_2
            routeID = route.routeID

        return self.aggregate(student_route_attendence, routeID)

    def get_days(self):
        month = self.kwargs.get('month')
        cal = calendar.Calendar()
        cal.setfirstweekday(6)
        year, month = list(map(int, month.split('-')))

        month_days = cal.itermonthdays(int(year), int(month))
        days = [int(day) for day in month_days]
        month_name = calendar.month_name[int(month)]
        return days, month_name

    def get_route(self):
        filter_id = self.kwargs.get('filter_id')
        filter_type = self.kwargs.get('filter_type')

        if filter_type == 'route':
            return Routes.objects.get(routeID=filter_id).route_code
        else:
            shift = StudentRoute.objects.filter(
                student__admissionNumber=filter_id).first().shift
            route = shift.route_code_1 or shift.route_code_2
            return route.route_code

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['days'], context['month'] = self.get_days()
        context['routes'] = Routes.objects.all()
        context['students'] = StudentRoute.objects.all()
        context['route_code'] = self.get_route()
        return context


class RouteAttendenceListPDF(PdfMixin, RouteAttendenceList):
    template_name = 'transport/routeAttendenceListPDF.html'


@login_required
def route_report(request):
    if request.method == "POST":
        routeID = 1
        route = Routes.objects.get(routeID=routeID)
        routes_list = RouteDetail.objects.filter(
            Q(route_code_2=route) | Q(route_code_1=route))
        student_routes_list = StudentRoute.objects.filter(
            shift__in=routes_list)
        # route_code = request.POST.get("route_code")
        # request.session["route_code"] = route_code
        # routes_list = Routes.objects.filter(route_code=route_code)
        # student_routes_list = StudentRoute.objects.filter(
        #     route_code=route_code)
        mylist = zip(routes_list, student_routes_list)
        return render(request, 'transport/report.html', {"routes": Routes.objects.all(), "my_list": mylist})
    return render(request, 'transport/report.html', {"routes": Routes.objects.all()})


@login_required
def route_report_pdf(request):
    """
    Export route report to pdf
    """
    route_code = request.session["route_code"]
    routes_list = Routes.objects.filter(route_code=route_code)
    student_routes_list = StudentRoute.objects.filter(route_code=route_code)
    mylist = zip(routes_list, student_routes_list)
    template_path = 'transport/routeReportPdf.html'
    context = {"my_list": mylist}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="route-report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render((context))

    # create a pdf
    pisaStatus = pisa.CreatePDF(
        html, dest=response)
    if pisaStatus.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


@login_required
def get_student_transport_route(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.user_type == "Student":
        addmission_number = user_profile.addmission_number
        student_route = StudentRoute.objects.get(
            student__admissionNumber=addmission_number)
        route_code = student_route.route_code
        route = Routes.objects.get(route_code=route_code)
        vehicle = route.vehicle
        driver = Driver.objects.get(vehicle=vehicle)
        context = {
            "student_route": student_route,
            "route": route,
            "driver": driver
        }
        return render(request, 'transport/getStudentRoute.html', context)
