from django.db import models

# Create your models here.


class BusinessImage(models.Model):
    file_name = models.TextField(blank=True, null=True)
    file_path = models.TextField(blank=True, null=True)
    cdn_link = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

class BusinessRegistration(models.Model):
    business_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    category = models.CharField(max_length=255)
    website = models.URLField(null=True, blank=True)
    street_name = models.CharField(max_length=255)
    city_zip = models.CharField(max_length=255)
    city1 = models.CharField(max_length=255)
    city2 = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    business_description = models.TextField()
    business_days_and_hours = models.TextField()
    images = models.ManyToManyField('BusinessImage',related_name='BusinessImages')

    def __str__(self):
        return self.business_name



class Keywords(models.Model):
    business = models.ForeignKey('BusinessRegistration', on_delete=models.CASCADE, related_name='keywords')
    keywords = models.CharField(max_length=255)

    def __str__(self):
        return self.keywords