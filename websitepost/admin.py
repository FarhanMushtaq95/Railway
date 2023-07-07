from django.contrib import admin
from .models import Category, City, Post, State, PostImage

# Register your models here.

admin.site.register(City)
admin.site.register(State)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostImage)

