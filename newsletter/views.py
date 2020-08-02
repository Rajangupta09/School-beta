from django.shortcuts import render, redirect
from .models import Newsletter
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

@login_required
def home(request):
    news = Newsletter.objects.all()
    if request.method == "GET":
        if 'star' in request.GET:
            star = request.GET.get("star")
            _id = request.GET.get("id")
            temp = Newsletter.objects.get(id=_id)
            if star == 'delete':
                temp.delete()
                messages.success(request, 'deleted Successfully.')
            else:
                temp.star = star
                temp.save()
        description = request.GET.get("description")
        if description:
            temp = Newsletter.objects.filter(description__iexact=description)
            if not temp:
                Newsletter.objects.create(description=description)
                messages.success(request, 'Uploaded Successfully.')
            else:
                messages.warning(request, "Newsletter already exists")
            redirect('/newsletter/')
    return render(request, 'newsletter/addNewsletter.html', {'news':news})