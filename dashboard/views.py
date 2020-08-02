from django.shortcuts import render, redirect
from dailythought.models import Thoughts
from newsletter.models import Newsletter
from gallery.models import Photo
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
import datetime
from random import randrange
from accounts.models import UserProfile
from schoolinfo.models import SchoolInfo

# Create your views here.
# 3rd party for encryption and decryption
# from Crypto.Cipher import AES
import base64
import os
from cryptography.fernet import Fernet

@login_required
def home(request):
    """
    Main view page of dashboard.

    """
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        thought = Thoughts.objects.all()
        news = Newsletter.objects.filter(date=datetime.date.today())
        if len(thought) > 0:
            if thought[0].timestamp != datetime.date.today():
                thought[0].timestamp = datetime.date.today()
                today_thought = thought[randrange(len(thought)-1)]
            else:
                today_thought = thought.last()

            context = {"thought": today_thought,
                       "news": news,
                       "profile": profile,
                       "school": SchoolInfo.objects.all(),
                       "photos": Photo.objects.all()
                       }
            return render(request, 'dashboard/dashboard.html', context)
        else:
            context = {
                "news": news,
                "profile": profile,
                "school": SchoolInfo.objects.all(),
                "photos": Photo.objects.all()
            }
            return render(request, 'dashboard/dashboard.html', context)
    else:
        return render(request, 'accounts/login.html')


@login_required
def profile(request):
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        if request.method == "POST":
            username = request.POST.get('username')
            name = request.POST.get('first_name')
            mobile_no = request.POST.get('phonenumber')
            profile.mobile_no = mobile_no
            profile.user.username = username
            request.user.username = username
            request.user.save()
            profile.fullName = name
            profile.save()
            if request.FILES.get("profile_picture"):
                profile.image = request.FILES.get('profile_picture')
            current_password = request.POST.get('current_password')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            if current_password:
                _user = auth.authenticate(
                    username=username, password=current_password)
                if _user is not None:
                    if password1 == password2:
                        request.user.set_password(password1)
                        request.user.save()
                        # to generate a key
                        # key = Fernet.generate_key()
                        # file = open('key.key', 'wb')
                        # file.write(key) # The key is type bytes still
                        # file.close()
                        # store the keys
                        file = open('key.key', 'rb')
                        key = file.read() # The key will be type bytes
                        file.close()
                        f = Fernet(key)
                        test_string = password1.encode()
                        # res = bytes(test_string, 'utf-8')
                        encrypt_value = f.encrypt(test_string)
                        print(encrypt_value)
                        profile.password = encrypt_value
                        profile.save()
                        messages.info(request, 'Login with your new password')
                        return redirect('/')
                else:
                    messages.error(request, "Passwords didn't match!")
                    redirect('userProfile')
            else:
                profile.save()
                return render(request, 'dashboard/profile.html', {'profile': profile})
        return render(request, 'dashboard/profile.html', {'profile': profile})
    else:
        return render(request, 'accounts/login.html')
