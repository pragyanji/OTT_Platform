from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import OTT_user,Movies,Subscription
# Register your models here.

admin.site.register(OTT_user,UserAdmin)
admin.site.register(Movies)
admin.site.register(Subscription)