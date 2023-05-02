from django.urls import path
from .views import BusinessView

urlpatterns = [
    path('crud/', BusinessView.as_view(), name='business_api'),  # override sjwt stock token
]