import csv
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions
from .models import BusinessRegistration,Category,Keywords
from .serializers import BusinessListSerializer,BusinessRegistrationSerializer , CategoryListSerializer, KeywordsListSerializer

class BusinessView(APIView):

    # This class is used for getting all Places
    def get(self, request):

        # Checking permissions

        id = request.GET.get('id', None)
        state = request.GET.get('state', None)
        zip = request.GET.get('zip', None)
        if id is not None:
            query_set = BusinessRegistration.objects.filter(id=id)
        elif state is not None:
            query_set = BusinessRegistration.objects.filter(state=state)
        elif zip is not None:
            query_set = BusinessRegistration.objects.filter(zip=zip)
        else:
            query_set = BusinessRegistration.objects.all().order_by('-id')

        if not query_set:
            data = []

            return Response(data, status=200)
        serializer = BusinessListSerializer(query_set, many=True)

        return Response(serializer.data, status=200)

    # this function is used for creating new Place
    def post(self, request):

        request_data = request.data
        business = BusinessRegistrationSerializer(data=request_data)
        if business.is_valid():
            business.save()

            return Response({"detail": "Business created"}, status=200)
        else:
            return Response(business.errors, status=422)

    # this function is used for editing Place
    def put(self, request):


        obj_id = request.data.get("id", None)
        request_data = request.data

        if obj_id is None:
            return Response({'detail': 'business id missing'}, status=404)
        else:
            place = BusinessRegistration.objects.filter(id=obj_id).first()
            serializer = BusinessRegistrationSerializer(place, data=request_data)

        if serializer.is_valid():
            serializer.save()

            return Response({"detail": "Business updated"}, status=200)
        else:
            return Response(serializer.errors, status=422)


class CategoryView(APIView):

    # This class is used for getting all Category
    def get(self, request):

        # Checking permissions

        id = request.GET.get('id', None)
        if id is not None:
            query_set = Category.objects.filter(id=id)
        else:
            query_set = Category.objects.all().order_by('-id')

        if not query_set:
            data = []

            return Response(data, status=200)
        serializer = CategoryListSerializer(query_set, many=True)

        return Response(serializer.data, status=200)


class KeywordView(APIView):

    # This class is used for getting all Places
    def get(self, request):

        # Checking permissions

        id = request.GET.get('id', None)
        if id is not None:
            query_set = Keywords.objects.filter(id=id)
        else:
            query_set = Keywords.objects.all().order_by('-id')

        if not query_set:
            data = []

            return Response(data, status=200)
        serializer = KeywordsListSerializer(query_set, many=True)

        return Response(serializer.data, status=200)