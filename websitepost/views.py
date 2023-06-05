from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Category, City, State
from .serializers import PostSerializer, CitySerializer, CategorySerializer, StateSerializer, PostcrudSerializer, PostListSerializer
from datetime import datetime
from authentication.models import SocialAccount,CustomUser as User

class CreatePostView(APIView):
    permission_classes = [permissions.IsAuthenticated] # Ensure user is authenticated

    def post(self, request):
        serializer = PostcrudSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() # Set the user as the currently logged in user
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class GetPostView(APIView):
    permission_classes = [] # Ensure user is authenticated
    def get(self, request):
        # Retrieve all posts from the database
        id = request.GET.get('id',None)
        if id:
            posts = Post.objects.filter(business_id=id,schedule_time__lte=datetime.now())
        else:
            posts = Post.objects.all()
        # Serialize the queryset to a list of serialized data
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data, status=200)


class GetCityView(APIView):
    permission_classes = [permissions.IsAuthenticated] # Ensure user is authenticated
    def get(self, request):
        # Retrieve all posts from the database
        id = request.GET.get('id',None)
        if id:
            posts = City.objects.filter(id=id)
        else:
            posts = City.objects.all()
        # Serialize the queryset to a list of serialized data
        serializer = CitySerializer(posts, many=True)
        return Response(serializer.data, status=200)


class GetStateView(APIView):
    permission_classes = [permissions.IsAuthenticated] # Ensure user is authenticated
    def get(self, request):
        # Retrieve all posts from the database
        id = request.GET.get('id',None)
        if id:
            posts = State.objects.filter(id=id)
        else:
            posts = State.objects.all()
        # Serialize the queryset to a list of serialized data
        serializer = StateSerializer(posts, many=True)
        return Response(serializer.data, status=200)


class GetCategoryView(APIView):
    permission_classes = [permissions.IsAuthenticated] # Ensure user is authenticated
    def get(self, request):
        # Retrieve all posts from the database
        id = request.GET.get('id',None)
        if id:
            posts = Category.objects.filter(id=id)
        else:
            posts = Category.objects.all()
        # Serialize the queryset to a list of serialized data
        serializer = CategorySerializer(posts, many=True)
        return Response(serializer.data, status=200)

class SignUpAPIView(APIView):
    permission_classes = []
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        website = request.data.get('website')

        # Check if the username already exists
        if User.objects.filter(email=username).exists():
            return Response({'error': 'Username already exists'})

        # Create the new user
        user = User.objects.create_user(email=username, password=password, username=username)
        website = SocialAccount.objects.create(user=user,provider=website,access_token='access_token')
        return Response({'success': 'User created'})