from django.urls import path, include
from .views import CreatePostView, GetPostView, GetCityView, GetStateView, GetCategoryView


urlpatterns = [
    # Simple Sign up
    path('create/', CreatePostView.as_view(), name='create'),
    path('get/', GetPostView.as_view(), name='get'),
    path('getcity/', GetCityView.as_view(), name='getcity'),
    path('getstate/', GetStateView.as_view(), name='getstate'),
    path('getcategory/', GetCategoryView.as_view(), name='getcategory'),


]