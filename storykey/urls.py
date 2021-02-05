from django.contrib import admin
from django.urls import path
from . import views
app_name = 'storykey'
urlpatterns = [
    path('storykey', views.storykey, name='storykey')
]
