from django.db import models

# Create your models here.
class content(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    desc = models.TextField()


class demo_book(models.Model):
    name = models.CharField(max_length=100)
    countryCode  = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
