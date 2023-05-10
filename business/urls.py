from django.urls import path
from .views import BusinessView , CategoryView, KeywordView

urlpatterns = [
    path('crud/', BusinessView.as_view(), name='business_api'),  # override sjwt stock token
    path('category/', CategoryView.as_view(), name='category_api'),
    path('keyword/', KeywordView.as_view(), name='keyword_api'),


]