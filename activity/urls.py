from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [

    path('watchmoon', views.watchmoon, name="watchmoon"),
    path('watchsunset', views.watchsunset, name="watchsunset"),
    path('watchgallery', views.watchgallery, name="watchgallery"),

]
