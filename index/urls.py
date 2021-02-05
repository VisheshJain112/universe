from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('index_case', views.index_case, name="index_case"),
]
