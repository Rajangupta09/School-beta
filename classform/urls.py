from django.urls import path
from . import views

urlpatterns = [
    path('', views.addclass, name="addClass"),
    path('Subject', views.addsubject, name="addsubject"),
]
