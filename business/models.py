from django.db import models

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name


class BusinessImage(models.Model):
    file_name = models.TextField(blank=True, null=True)
    file_path = models.TextField(blank=True, null=True)
    cdn_link = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)


class Keywords(models.Model):
    keywords = models.CharField(max_length=255)

    def __str__(self):
        return self.keywords


class BusinessRegistration(models.Model):
    business_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='business_category')
    website = models.URLField(null=True, blank=True)
    street_name = models.CharField(max_length=255)
    city_zip = models.CharField(max_length=255)
    city1 = models.CharField(max_length=255)
    city2 = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    business_description = models.TextField()
    business_days_and_hours = models.TextField()
    images = models.ManyToManyField('BusinessImage',related_name='BusinessImages')
    keyword = models.ManyToManyField('Keywords', related_name='businesskeywords')

    def __str__(self):
        return self.business_name





class BusinessHour(models.Model):
    DAY_CHOICES = [
        ('mon', 'Monday'),
        ('tue', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thu', 'Thursday'),
        ('fri', 'Friday'),
        ('sat', 'Saturday'),
        ('sun', 'Sunday'),
    ]

    business = models.ForeignKey(BusinessRegistration, on_delete=models.CASCADE, related_name='business_hours')
    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    closed = models.BooleanField(default=False)

    def __str__(self):
        return self.business.business_name