from django.contrib import admin
from .models import AD_User
from .models import AD_Admin
# Register your models here.
admin.site.register(AD_User)
admin.site.register(AD_Admin)