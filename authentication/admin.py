from django.contrib import admin
from .models import CustomUser,SocialAccount
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(SocialAccount)
