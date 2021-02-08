from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('ch1', views.ch1, name="ch1"),
    path('ch2', views.ch1, name="ch2"),
    path('ch3', views.ch1, name="ch3"),
    path('ch4', views.ch1, name="ch4"),

]
