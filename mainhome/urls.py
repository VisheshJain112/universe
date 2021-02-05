from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index_home, name="index_home"),
    path('mainhome', views.mainhome, name="mainhome"),
]
