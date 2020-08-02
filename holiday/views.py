from django.shortcuts import render, redirect
from datetime import date
from .models import Holidays
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from classform.models import ClassRoom

# Create your views here.
@login_required
def add_holiday(request):
    if request.method == "POST":
        if 'student' in request.POST:
            day = request.POST['holiday']
            classh = request.POST['Hclass']
            classroom = ClassRoom.objects.get(classSection=classh)
            holiday = Holidays.objects.create(
                holiday_date=day, holiday_date_to=day, classroom=classroom, category='student')
            messages.success(request, "Marked Holiday")
        if 'employee' in request.POST:
            day = request.POST['holiday']
            cat = request.POST['Ecategory']
            holiday = Holidays.objects.create(
                holiday_date=day, holiday_date_to=day, employeeholiday=cat, category='employee')
            messages.success(request, "Marked Holiday")
    return redirect('/dashboard')
