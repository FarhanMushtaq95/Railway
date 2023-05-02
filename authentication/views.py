from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import  TokenObtainPairSerializer


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class HelloWorldView(APIView):

    def get(self, request):
        return Response(data={"hello":"world"}, status=200)