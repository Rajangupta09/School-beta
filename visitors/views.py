from django.shortcuts import render, redirect
from .models import Visitor
from django.contrib import messages
from datetime import date
from datetime import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
	if request.method == "POST":
		name = request.POST.get("name")
		mobile_no = request.POST.get("mobile_no")
		address = request.POST.get("address")
		contact_to = request.POST.get("contact_to")
		purpose = request.POST.get("purpose")
		photos = request.FILES.get("photos")
		document = request.FILES.get("document")
		if photos and document:
			Visitor.objects.create(name=name, mobile_no=mobile_no, address=address, purpose=purpose, photo=photos, document=document,contact_to=contact_to, date_time=datetime.now())
		else:
			Visitor.objects.create(name=name, mobile_no=mobile_no, address=address, purpose=purpose, contact_to=contact_to, date_time=datetime.now())
		messages.success(request, "Visitor detail added!")
		redirect("visitorForm")
	return render(request, 'visitors/home.html')

@login_required
def visitor_list(request):
	vmonth = '2020-01'
	if request.method == "POST":
		_date = request.POST.get("date")
		vmonth = request.POST.get("month")
		_month = vmonth.split('-')
		if _date:
			_date = date(*map(int, _date.split('-')))
			visitors = Visitor.objects.filter(date_time__date=_date)
		else:
			visitors = Visitor.objects.filter(date_time__year=_month[0])
			visitors = visitors.filter(date_time__month=_month[1])
		return render(request, 'visitors/visitor_list.html', {"visitors":visitors, 'vmonth':vmonth})
	return render(request, 'visitors/visitor_list.html', {'vmonth':vmonth})