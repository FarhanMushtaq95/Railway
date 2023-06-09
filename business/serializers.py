
from rest_framework import serializers
from .models import BusinessRegistration, BusinessImage, Keywords , Category, BusinessHour


import pyrebase
import os
from dotenv import load_dotenv

load_dotenv()
# Create your views here.



"""firebaseConfig = {
  "apiKey": "AIzaSyByytUPV4CAkrTSLWpNypP73vloZvuh81Y",
  "authDomain": "ads-7049d.firebaseapp.com",
  "projectId": "ads-7049d",
  "storageBucket": "ads-7049d.appspot.com",
  "messagingSenderId": "229131621527",
  "appId": "1:229131621527:web:385c2b7287faafb5ad05d2",
  "measurementId": "G-CYM0FQ86XQ",
    "databaseURL":""
}"""
firebase_config = {
  "apiKey": os.getenv("API_KEY"),
  "authDomain": os.getenv("AUTH_DOMAIN"),
  "projectId": os.getenv("PROJECT_ID"),
  "storageBucket": os.getenv("STORAGE_BUCKET"),
  "messagingSenderId": os.getenv("MESSAGING_SENDER_ID"),
  "appId": os.getenv("APP_ID"),
  "measurementId": os.getenv("MEASUREMENT_ID"),
  "databaseURL": ""
}
firebase = pyrebase.initialize_app(firebase_config)
storage = firebase.storage()

class BusinessHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessHour
        fields = ('day', 'opening_time', 'closing_time', 'closed')


class BusinessRegistrationSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(), write_only=True,required=False)
    business_days_and_hours = BusinessHoursSerializer(many=True, required=False)

    class Meta:
        model = BusinessRegistration
        fields = '__all__'

    def create(self, validated_data):
        images_data = validated_data.pop('images', None)
        keywords = validated_data.pop('keyword',None)
        day_and_business = validated_data.pop('business_days_and_hours',None)
        business = BusinessRegistration.objects.create(**validated_data)

        if images_data:
            for image_data in images_data:
                media = BusinessImage()
                firebase_data = storage.child("files/" + image_data.name).put(image_data)
                media.file_path = storage.child("files/" + image_data.name).get_url(firebase_data['generation'])
                media.cdn_link = storage.child("files/" + image_data.name).get_url(firebase_data['generation'])
                media.file_name = image_data.name
                media.deleted = False
                media.deleted_at = None
                media.save()
                business.images.add(media)
        if keywords:
            business.keyword.set(keywords)
        if day_and_business is None:
            var = [
                    {
                            "day": "MON",
                            "open_time": "09:00:00",
                            "close_time": "17:00:00",
                            "closed": False
                    },
                    {
                        "day": "TUE",
                        "open_time": "09:00:00",
                        "close_time": "17:00:00",
                        "closed": False
                    },
                    {
                        "day": "WED",
                        "open_time": "09:00:00",
                        "close_time": "17:00:00",
                        "closed": False
                    },
                    {
                        "day": "THU",
                        "open_time": "09:00:00",
                        "close_time": "17:00:00",
                        "closed": False
                    },
                    {
                        "day": "FRI",
                        "open_time": "09:00:00",
                        "close_time": "17:00:00",
                        "closed": False
                    },
                    {
                        "day": "SAT",
                        "open_time": None,
                        "close_time": None,
                        "closed": True
                    },
                    {
                        "day": "SUN",
                        "open_time": None,
                        "close_time": None,
                        "closed":True
                    }
            ]
            for obj in var:
                bus = BusinessHour.objects.create(business=business,day=obj['day'],opening_time=obj['open_time'],closing_time=obj['close_time'],closed=obj['closed'])
                business.business_days_and_hours.add(bus)
                business.save()
        else:
            for obj in day_and_business:
                bus = BusinessHour.objects.create(business=business,day=obj['day'],opening_time=obj['open_time'],closing_time=obj['close_time'],closed=obj['closed'])
                business.business_days_and_hours.add(bus)
                business.save()
        return business
    def update(self, instance, validate_data):
        validated_data = self.initial_data
        images_data = validated_data.pop('images', None)
        keywords = validated_data.pop('keyword', None)
        BusinessRegistration.objects.filter(id=instance.id).update(**validated_data)
        business = BusinessRegistration.objects.get(id=instance.id)
        if images_data:
            for image_data in images_data:
                media = BusinessImage()
                firebase_data = storage.child("files/" + image_data.name).put(image_data)
                media.file_path = storage.child("files/" + image_data.name).get_url(firebase_data['generation'])
                media.cdn_link = storage.child("files/" + image_data.name).get_url(firebase_data['generation'])
                media.file_name = image_data.name
                media.deleted = False
                media.deleted_at = None
                media.save()
                business.images.set(media)
        if keywords:
            business.keyword.set(keywords)
        return instance


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class KeywordsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keywords
        fields = '__all__'


class BusinessMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessImage
        fields = ('id', 'cdn_link')


class BusinessListSerializer(serializers.ModelSerializer):
    keywords = serializers.SerializerMethodField('get_keywords')
    Media = serializers.SerializerMethodField('get_Media')
    business_days_and_hours = BusinessHoursSerializer(many=True, required=False)


    class Meta:
        model = BusinessRegistration
        fields = '__all__'

    def get_keywords(self, obj):
        data = {}
        serializer_context = {'request': self.context.get('request')}
        keywords_data = Keywords.objects.filter(businesskeywords=obj)
        serializer = KeywordsListSerializer(keywords_data, many=True, context=serializer_context)
        try:
            return serializer.data
        except:
            return data

    def get_Media(self, obj):
        data = {}
        serializer_context = {'request': self.context.get('request')}
        media_data = BusinessImage.objects.filter(BusinessImages=obj)
        serializer = BusinessMediaSerializer(media_data, many=True, context=serializer_context)
        try:
            return serializer.data
        except:
            return data