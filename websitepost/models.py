from django.db import models
import authentication.models as Auth
import business.models as Bus

# Create your models here.

class PostImage(models.Model):
    file_name = models.TextField(blank=True, null=True)
    file_path = models.TextField(blank=True, null=True)
    cdn_link = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

class Category(models.Model):
    name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class State(models.Model):
    name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class City(models.Model):
    name = models.CharField(max_length=150)
    state = models.ForeignKey(State,on_delete=models.CASCADE,related_name="city_state")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=500)
    email = models.EmailField()
    number = models.CharField(max_length=50)
    category = models.ForeignKey(Category,on_delete=models.CASCADE, related_name="post_category")
    state = models.ForeignKey(State,on_delete=models.CASCADE,related_name="post_state")
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="post_city")
    schedule_time = models.DateTimeField(null=True)
    business = models.ForeignKey(Bus.BusinessRegistration, on_delete=models.CASCADE, related_name="business_post",null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    images = models.ManyToManyField('PostImage',related_name='PostImages')

    def __str__(self):
        return self.title

class Review(models.Model):
    comment = models.CharField(max_length=356)
    comment_by = models.ForeignKey(Auth.CustomUser, on_delete=models.CASCADE, related_name="user_comment")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comment")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
