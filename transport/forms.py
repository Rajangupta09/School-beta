from django import forms
from .models import (Driver, Vehicle, Routes, Stoppage,
                     RouteVehicle, RouteDetail)
from employeeform.models import Employee
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
from datetime import datetime, date as Date
from holiday.models import Holidays

# from classform.forms import StudentRouteAttendenceForm


class CrispyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_form_helper()

    def init_form_helper(self):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True


class NestedEmployeeForm(CrispyForm):
    def init_form_helper(self):
        super().init_form_helper()
        self.helper.layout = Layout(
            Div(
                Field('firstName', wrapper_class="col-md-3"),
                Field('lastName', wrapper_class="col-md-3"),
                Field('dob', wrapper_class="col-md-3"),
                Field('mobile_number', wrapper_class="col-md-3"),
                css_class='form-row fieldset'
            ),
            Div(
                Field('currentAddress', wrapper_class="col-md-3"),
                Field('permanentAddress', wrapper_class="col-md-3"),
                css_class='form-row fieldset'
            ),
        )

    class Meta:
        model = Employee
        fields = [
            'dob',
            'currentAddress',
            'permanentAddress',
            'mobile_number',
            'firstName',
            'lastName'
        ]


class DriverUpdateForm(CrispyForm):

    class VehicleModelChoiceField(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return f"{obj.vehicle_no}"

    vehicle = VehicleModelChoiceField(queryset=Vehicle.objects.all())

    def __init__(self, *args, employeeInstance=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.employee = employeeInstance
        self.init_employee_form()

        self.fields['driverID'].required = False
        self.fields['driverPic'].required = False
        self.fields['vehicle'].widget.attrs['class'] = 'form-control mr-2'

    def init_employee_form(self):
        self.employeeForm = NestedEmployeeForm(
            data=self.data if self.is_bound else None,
            files=self.files if self.is_bound else None,
            instance=self.employee
        )

    def init_form_helper(self):
        super().init_form_helper()
        self.helper.layout = Layout(
            Div(
                Field('vehicle', wrapper_class="col-md-3"),
                Field('batch_no', wrapper_class="col-md-3"),
                Field(
                    'driverLicense',
                    css_class='form-control',
                    wrapper_class="col-md-3"
                ),
                Field(
                    'driverPic',
                    css_class='form-control',
                    wrapper_class="col-md-3"
                ),
                css_class='form-row'
            ),
            Div(
                Field(
                    'driverID',
                    css_class='form-control',
                    wrapper_class="col-md-3"
                ),
                Field(
                    'license_no',
                    wrapper_class="col-md-3"
                ),
                css_class='form-row'
            ),
        )

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.employee = self.employee
        instance.save()
        return instance

    class Meta:
        model = Driver
        exclude = ('employee',)


class StoppageForm(CrispyForm):

    def init_form_helper(self):
        super().init_form_helper()
        self.helper.layout = Layout(
            Div(
                Field('stoppage_name', wrapper_class="col-md-3"),
                Field('longitude', wrapper_class="col-md-3"),
                Field('lattitude', wrapper_class="col-md-3"),
                Field('DELETE', wrapper_class="col-md-3 mt-4",),
                css_class="form-row fieldset"
            ),
        )

    class Meta:
        model = Stoppage
        exclude = ('route_detail',)


class RouteVehicleForm(CrispyForm):
    def init_form_helper(self):
        super().init_form_helper()
        self.helper.layout = Layout(
            Div(
                Field('vehicle', wrapper_class="col-md-3"),
                css_class="form-row fieldset"
            ),
        )

    class Meta:
        model = RouteVehicle
        exclude = ('route',)


class RouteDetailForm(CrispyForm):
    """
        inverse field mapping for shift 2
        where start and end values are interchanged
    """
    reverse_field_mapping = {
        'start_place': 'end_place',
        'end_place': 'start_place',
        'start_lattitude': 'end_lattitude',
        'end_lattitude': 'start_lattitude',
        'start_longitude': 'end_longitude',
        'end_longitude': 'start_longitude',
        'remarks': 'remarks',
        'route_distance': 'route_distance'
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_stoppage_formset()
        self.fields['remarks'].required = False
        self.fields['route_distance'].required = False

    def init_form_helper(self):
        super().init_form_helper()
        self.helper.layout = Layout(
            Div(
                Field('start_place', wrapper_class="col-md-3"),
                Field('start_lattitude', wrapper_class="col-md-3"),
                Field('start_longitude', wrapper_class="col-md-3"),
                css_class="form-row fieldset"
            ),
            Div(
                Field('end_place', wrapper_class="col-md-3"),
                Field('end_lattitude', wrapper_class="col-md-3"),
                Field('end_longitude', wrapper_class="col-md-3"),
                css_class="form-row fieldset"
            ),
            Div(
                Field('route_distance', wrapper_class="col-md-3"),
                Field('remarks', wrapper_class="col-md-3"),
                css_class="form-row fieldset"
            ),
        )

    def init_stoppage_formset(self):
        stoppage_formset_factory = forms.inlineformset_factory(
            RouteDetail,
            Stoppage,
            form=StoppageForm,
            extra=1
        )

        self.stoppage_formset = stoppage_formset_factory(
            data=self.data if self.is_bound else None,
            files=self.files if self.is_bound else None,
            instance=self.instance
        )

    def reverse_stoppages(self, stoppages, instance: RouteDetail):
        """
        creates new stoppages and saves them in reverse order for route detail instance
        """
        for stoppage in stoppages[::-1]:
            stoppage.id = None
            stoppage.route_detail = instance
            stoppage.save()

    def save(
        self,
        commit=True,
        save_stoppages=True,
        reverse_stoppages=False,
        override_instance=False,
        detail_instance: RouteDetail = None,
    ):
        instance = super().save(commit=commit)

        if not save_stoppages:
            return instance

        stoppages = None
        if override_instance:
            assert detail_instance is not None
            self.stoppage_formset.instance = detail_instance
        else:
            self.stoppage_formset.instance = self.instance

        if self.stoppage_formset.is_valid():
            stoppages = self.stoppage_formset.save(
                commit=not reverse_stoppages
            )
            if reverse_stoppages:
                self.reverse_stoppages(stoppages, detail_instance)
        else:
            raise forms.ValidationError(self.route_vehicle_formset.errors)

        return instance

    class Meta:
        model = RouteDetail
        exclude = ('route_code_1', 'route_code_2',
                   'sub_route_code', 'archived')


class RouteForm(CrispyForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_route_vehicle_formset()
        self.init_detail_form()

    def init_form_helper(self):
        super().init_form_helper()
        self.helper.layout = Layout(
            Div(
                Field('route_code', wrapper_class="col-md-3"),
                Field('shift_time', wrapper_class="col-md-3"),
                css_class="form-row fieldset"
            ),
        )

    def init_route_vehicle_formset(self):
        route_vehicle_formset_factory = forms.inlineformset_factory(
            Routes,
            RouteVehicle,
            form=RouteVehicleForm,
            extra=1
        )

        self.route_vehicle_formset = route_vehicle_formset_factory(
            data=self.data if self.is_bound else None,
            files=self.files if self.is_bound else None,
            instance=self.instance
        )

    def init_detail_form(self):
        self.detail_form = RouteDetailForm(
            data=self.data if self.is_bound else None,
            files=self.files if self.is_bound else None,
        )

    def get_instance2(self, instance: RouteDetail):
        """
        makes new detail instance with start and end palces data swaped
        and route_code(s) set to None
        input: orignal instance
        """
        new_detail = RouteDetail.objects.get(id=instance.id)
        new_detail.id = None
        new_detail.route_code_1, new_detail.route_code_2 = None, None
        new_detail.start_place, new_detail.end_place = instance.end_place, instance.start_place
        new_detail.start_lattitude = instance.end_lattitude
        new_detail.start_longitude = instance.end_longitude
        new_detail.end_lattitude = instance.start_lattitude
        new_detail.end_longitude = instance.start_longitude
        return new_detail

    def save_detail_form(self, route_instance: Routes):
        """
        checks the shift time for new route.
        if shift == BOTH:
            makes a new detail instance called new_detail where start and end
            palces are swaped and saves it assuming orignal detail were for morning
            shift
        """
        if self.detail_form.is_valid():
            detail_instance: RouteDetail = self.detail_form.save(
                commit=False,
                save_stoppages=False
            )
            new_detail: RouteDetail = None
            shift_time = route_instance.shift_time

            """
            To copy an django model object you have to first save it to the database
            which leads to this weired code structure
            """

            if shift_time == Routes.Shift.MORNING or shift_time == Routes.Shift.BOTH:
                detail_instance.route_code_1 = route_instance
                detail_instance.sub_route_code = f"{route_instance.route_code}-a"
                detail_instance.save()
                if shift_time == Routes.Shift.BOTH:
                    new_detail = self.get_instance2(detail_instance)
                    new_detail.route_code_2 = route_instance
                    new_detail.sub_route_code = f"{route_instance.route_code}-b"
                    new_detail.save()

            elif shift_time == Routes.Shift.AFTERNOON:
                detail_instance.route_code_2 = route_instance
                detail_instance.sub_route_code = f"{route_instance.route_code}-b"
                detail_instance.save()

            self.detail_form.save(
                commit=False,
                override_instance=True,
                detail_instance=detail_instance
            )
            if new_detail:
                self.detail_form.save(
                    commit=False,
                    override_instance=True,
                    detail_instance=new_detail,
                    reverse_stoppages=True
                )
        else:
            raise forms.ValidationError(self.detail_form.errors)

    def save_route_vehicles_formset(self, route_instance: Routes):
        self.route_vehicle_formset.instance = route_instance
        if self.route_vehicle_formset.is_valid():
            self.route_vehicle_formset.save()
        else:
            raise forms.ValidationError(self.route_vehicle_formset.errors)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.save()
        self.save_route_vehicles_formset(instance)
        self.save_detail_form(instance)

        return instance

    class Meta:
        model = Routes
        exclude = ('routeID', 'archived')


class RouteUpdateForm(RouteForm):

    add_detail_form = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['shift_time'].disabled = 'disabled'
        self.fields['shift_time'].required = False

    def init_detail_form(self, *args, **kwargs):
        """
        only displayed if current shift is morning or afternoon
        """

        if self.instance.shift_time != Routes.Shift.BOTH:
            self.detail_form_title = Routes.Shift.AFTERNOON if self.instance.shift_time == Routes.Shift.MORNING else Routes.Shift.MORNING
            return super().init_detail_form(*args, **kwargs)
        else:
            pass

    def save_detail_form(self, instance: Routes):
        if not self.cleaned_data.get('add_detail_form'):
            return

        detail_instance: RouteDetail = self.detail_form.save(
            commit=False, save_stoppages=False
        )
        current_shift = self.instance.shift_time

        if current_shift == Routes.Shift.AFTERNOON:
            """saving new shift as morning shift"""
            detail_instance.route_code_1 = instance
            detail_instance.sub_route_code = f'{instance.route_code}-a'
        else:
            """saving new shift as afternoon shift"""
            detail_instance.route_code_2 = instance
            detail_instance.sub_route_code = f'{instance.route_code}-b'

        instance.shift_time = Routes.Shift.BOTH
        instance.save()
        detail_instance.save()

        self.detail_form.save(
            commit=False,
            override_instance=True,
            detail_instance=detail_instance
        )

    def update_sub_route_code(self, instance: Routes):
        if hasattr(instance, 'morning_shift'):
            instance.morning_shift.sub_route_code = f'{instance.route_code}-a'
            instance.morning_shift.save()
        if hasattr(instance, 'afternoon_shift'):
            instance.afternoon_shift.sub_route_code = f'{instance.route_code}-b'
            instance.afternoon_shift.save()

    def form_invalid(self, *args, **kwargs):
        print("##############")
        print(self.errors)
        print(self.non_field_errors)

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)

        if 'route_code' in self.changed_data:
            self.update_sub_route_code(instance)


class RouteDetailUpdateForm(RouteDetailForm):

    sync_changes = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.route = self.instance.route_code_1 or self.instance.route_code_2
        self.add_sync_checkbox()

    def add_sync_checkbox(self):
        """
            used to add a checkbox which allows you to sync
            changes made to this shift to another shift if
            there are 2 shifts to this route
        """
        if self.route.shift_time != Routes.Shift.BOTH:
            return

        sync_label = Routes.Shift.AFTERNOON if self.instance.route_code_1 else Routes.Shift.MORNING
        self.fields['sync_changes'].label = f"Apply changes to {sync_label} shift"

        self.helper.layout.append(
            Div(
                Field('sync_changes', wrapper_class="pl-2 form-check"),
                css_class="form-row"
            ),
        )

    def sync(self, instance: RouteDetail):
        shift_2 = self.route.afternoon_shift if instance.route_code_1 else self.route.morning_shift
        for field in self.changed_data:
            if field == 'sync_changes':
                continue
            field_value = getattr(instance, field)
            reverse_field = self.reverse_field_mapping.get(field)
            setattr(shift_2, reverse_field, field_value)
        shift_2.save()

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)

        if self.cleaned_data.get('sync_changes'):
            self.sync(instance)


class StudentRouteAttendenceFormSet(forms.BaseInlineFormSet):

    def add_fields(self, form, index):
        fields = super().add_fields(form, index)
        classroom = self.instance.student.classroom_student.classRoom

        try:
            holiday = classroom.holidays_class.get(
                holiday_date=datetime.today().date())
        except Holidays.DoesNotExist:
            holiday = None

        if holiday:
            # form.fields['status'].widget.attrs['initial'] = ''
            form.fields['status'].widget.attrs['disabled'] = True
            form.fields['status'].label = "Holiday"

        return fields

    def get_queryset(self):
        queryset = super().get_queryset()
        today = Date.today()
        return queryset.filter(
            date__year=today.year,
            date__month=today.month,
            date__day=today.day
        )
