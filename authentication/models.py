from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    social_accounts = models.ManyToManyField('SocialAccount', blank=True)
    groups = models.ManyToManyField(
        Group,
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='customuser_set', # add related_name
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_set', # add related_name
        related_query_name='customuser',
    )


class SocialAccount(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    provider = models.CharField(max_length=50)
    provider_id = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'provider')
