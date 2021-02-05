from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('user_ui', views.user_ui, name="user_ui"),
]
