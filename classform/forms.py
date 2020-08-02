from django import forms
from .models import StudentRouteAttendence


class StudentRouteAttendenceForm(forms.ModelForm):

    STATUS_CHOICES = [
        ('present', "Present"),
        ('absent', "Absent"),
        ('late', "Late"),
        ('leave', "Leave"),
    ]

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        label='',
        widget=forms.RadioSelect,
    )

    def clean_status(self):
        data = self.cleaned_data["status"]
        # means holiday for student
        if self.fields['status'].widget.attrs.get('disabled') == True:
            return 'holiday'
        return data

    class Meta:
        model = StudentRouteAttendence
        exclude = ('date', 'time')
