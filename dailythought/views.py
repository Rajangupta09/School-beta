from django.shortcuts import render, redirect
from .models import Thoughts
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def add_thought(request):
    thoughts = Thoughts.objects.all()
    if request.method=="GET":
        if 'id' in request.GET:
            id = request.GET.get('id')
            temp = Thoughts.objects.get(id=id)
            temp.delete()
            
        thought = request.GET.getlist("thought")
        if thought:
            for i in thought:
                temp = Thoughts.objects.filter(thought__iexact=i)
                if not temp:
                    Thoughts.objects.create(thought=i, timestamp = datetime.datetime.today())
                else:
                    messages.warning(request, "Thought already Exists")
                    redirect('/thought/')
    return render(request, 'dailythought/addThought.html', {'thoughts' : thoughts})