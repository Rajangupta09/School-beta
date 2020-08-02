from django.shortcuts import render
from .models import SchoolInfo
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

@login_required
def home(request):
    if request.method == "POST":
        schoolName = request.POST.get("school_name")
        addresss = request.POST.get("address")
        principalName = request.POST.get("principal_name")
        email = request.POST.get("email")
        city = request.POST.get("inputCity")
        state = request.POST.get("inputState")
        zipCode = request.POST.get("inputZip")
        if not zipCode:
            zipCode = None
        schoolID = request.POST.get("school_id")
        if not schoolID:
            schoolID = None
        longitude = request.POST.get("longitude")
        if not longitude:
            longitude = None
        latitude = request.POST.get("latitude")
        if not latitude:
            latitude = None
        contactNumber = request.POST.get("conact_number")
        if not contactNumber:
            contactNumber = None
        webSiteURL = request.POST.get("web_url")
        img = request.FILES.get("school_img")
        logo = request.FILES.get("school_logo")
        try:
            SchoolInfo.objects.create(schoolName=schoolName, schoolID=schoolID, email=email, principalName=principalName,
                                  city=city, zipCode=zipCode, logo=logo, img=img, longitude=longitude, latitude=latitude, contactNumber=contactNumber, webSiteURL=webSiteURL, addresss=addresss, state=state)
            messages.success(request, 'School Detail Uploaded Successfully.')
        except:
            messages.warning(request, 'Couldnot Upload the Details!')
    return render(request, 'schoolinfo/addSchoolInfo.html')
