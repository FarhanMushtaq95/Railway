from django.contrib import admin
from .models import BusinessRegistration,BusinessImage,Category,Keywords
# Register your models here.

admin.site.register(BusinessRegistration)
admin.site.register(BusinessImage)
admin.site.register(Category)
admin.site.register(Keywords)