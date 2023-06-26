from django.urls import path, include
from .views import CreatePostView, GetPostView, GetCityView, GetStateView, GetCategoryView, SignUpAPIView, UpdatePostView


urlpatterns = [
    # Simple Sign up
    path('create/', CreatePostView.as_view(), name='create'),
    path('get/', GetPostView.as_view(), name='get'),
    path('update/', UpdatePostView.as_view(), name='update'),
    path('getcity/', GetCityView.as_view(), name='getcity'),
    path('getstate/', GetStateView.as_view(), name='getstate'),
    path('getcategory/', GetCategoryView.as_view(), name='getcategory'),
    path('signup/', SignUpAPIView.as_view(), name='signup'),


]