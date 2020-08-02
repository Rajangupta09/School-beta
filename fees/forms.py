from django import forms

# models
from .models import (
    FeeCategory, FeeCycle, FeeConfiguration,
    FeeDiscount, StudentDiscount, FeeHeadMapping, StudentDiscountThrough
)
from classform.models import ClassRoom, ClassRoomStudent
from form.models import StudentInfo

# utils import
from six import text_type
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
import calendar
from django.db.models import Q


class FeeCategoryForm(forms.ModelForm):

    class Meta:
        model = FeeCategory
        fields = ('name', 'submission_mode', 'deduction_order')


class FeeCycleForm(forms.ModelForm):

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        year = cleaned_data['session'].start.year
        month = cleaned_data['starting_month']
        month_range = calendar.monthrange(year, month)[1]
        if cleaned_data['last_submission_date'] > month_range:
            raise forms.ValidationError(
                {'last_submission_date': ["Enter a valid date value"]})
        return cleaned_data

    class Meta:
        model = FeeCycle
        fields = ('cycle', 'session', 'starting_month', 'last_submission_date')


class FeeConfigurationForm(forms.ModelForm):

    class FeeCategoryModelChoiceField(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return f"{obj.name}"

    fee_category = FeeCategoryModelChoiceField(
        queryset=FeeCategory.objects.all()
    )

    classrooms = forms.ModelMultipleChoiceField(
        queryset=ClassRoom.objects.all(),
        label='',
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'class-checkbox-item'}),
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = FeeConfiguration
        fields = "__all__"


class FeeDiscountForm(forms.ModelForm):

    fee_categories = forms.ModelMultipleChoiceField(
        queryset=FeeCategory.objects.all(),
        label='',
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'fee-category-checkbox-item'}),
        required=True
    )

    class Meta:
        model = FeeDiscount
        fields = "__all__"


class StudentDiscountForm(forms.ModelForm):
    student = forms.ModelMultipleChoiceField(
        queryset=StudentInfo.objects.all(),
        label='',
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'student-checkbox-item'}),
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = StudentDiscount
        fields = "__all__"


class FeeHeadMappingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].label = self.instance.fee_category.name

    class Meta:
        model = FeeHeadMapping
        fields = ('amount',)


class FeeHeadMappingFormset(forms.BaseInlineFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['instance'] = self.queryset[index]
        return kwargs


class StudentDiscountThroughForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].label = self.instance.discount.discount_category.discount_category

    class Meta:
        model = StudentDiscountThrough
        fields = ('amount',)


class StudentDiscountFormSet(forms.BaseInlineFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['instance'] = self.queryset[index]
        return kwargs


class FeeHeadMasterForm(forms.Form):
    def __init__(self, *args, student_instance=None, month=1, **kwargs):
        super().__init__(*args, **kwargs)
        self.student_instance = student_instance
        self.month = month
        self.init_fee_head_formset()
        self.init_student_discount_formset()

    def init_fee_head_formset(self):
        object_list = FeeHeadMapping.objects.filter(
            Q(student=self.student_instance) & Q(month=self.month))
        count = object_list.count()
        formset_factory = forms.inlineformset_factory(
            StudentInfo,
            FeeHeadMapping,
            form=FeeHeadMappingForm,
            formset=FeeHeadMappingFormset,
            min_num=count,
            max_num=count,
            can_delete=False,
        )

        self.fee_head_formset = formset_factory(
            self.data if self.is_bound else None,
            self.files if self.is_bound else None,
            instance=self.student_instance,
            queryset=object_list,
            prefix='feehead',
        )

    def init_student_discount_formset(self):
        object_list = self.student_instance.fee_discounts.all()
        count = object_list.count()
        formset_factory = forms.inlineformset_factory(
            StudentInfo,
            StudentDiscountThrough,
            formset=StudentDiscountFormSet,
            form=StudentDiscountThroughForm,
            min_num=count,
            max_num=count,
            can_delete=False,
        )

        self.student_discount_formset = formset_factory(
            self.data if self.is_bound else None,
            self.files if self.is_bound else None,
            instance=self.student_instance,
            prefix='discount',
            queryset=object_list
        )

    def save(self, *args, **kwargs):
        if self.fee_head_formset.is_valid():
            self.fee_head_formset.save()
        else:
            forms.ValidationError(self.fee_head_formset.errors)
        if self.student_discount_formset.is_valid():
            self.student_discount_formset.save()
        else:
            forms.ValidationError(self.student_discount_formset.errors)
