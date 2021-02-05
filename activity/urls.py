from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [

    path('watchmoon', views.watchmoon, name="watchmoon"),
    path('watchsunset', views.watchsunset, name="watchsunset"),
    path('watchgallery', views.watchgallery, name="watchgallery"),
    path('playbedroom', views.playbedroom, name="playbedroom"),
    path('readbook', views.readbook, name="readbook"),
    path('playmusic', views.playmusic, name="playmusic"),

]
