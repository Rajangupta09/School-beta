from django import forms
from employeeform.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Submit

class EmployeeRegistrationForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('__all__')