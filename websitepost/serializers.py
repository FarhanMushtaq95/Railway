from rest_framework import serializers
from .models import Post, Category, City, State, PostImage
from dotenv import load_dotenv
import os
import pyrebase

load_dotenv()
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

class PostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('id', 'cdn_link')

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'description', 'address', 'email', 'number', 'category', 'state', 'city','business', 'schedule_time']

class PostcrudSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(), write_only=True)

    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        images_data = validated_data.pop('images', None)
        post = Post.objects.create(**validated_data)

        if images_data:
            for image_data in images_data:
                media = PostImage()
                firebase_data = storage.child("files/" + image_data.name).put(image_data)
                media.file_path = storage.child("files/" + image_data.name).get_url(firebase_data['generation'])
                media.cdn_link = storage.child("files/" + image_data.name).get_url(firebase_data['generation'])
                media.file_name = image_data.name
                media.deleted = False
                media.deleted_at = None
                media.save()
                post.images.add(media)

        return post
    def update(self, instance, validate_data):
        validated_data = self.initial_data
        images_data = validated_data.pop('images', None)
        keywords = validated_data.pop('keyword', None)
        Post.objects.filter(id=instance.id).update(**validated_data)
        business = Post.objects.get(id=instance.id)
        if images_data:
            for image_data in images_data:
                media = PostImage()
                firebase_data = storage.child("files/" + image_data.name).put(image_data)
                media.file_path = storage.child("files/" + image_data.name).get_url(firebase_data['generation'])
                media.cdn_link = storage.child("files/" + image_data.name).get_url(firebase_data['generation'])
                media.file_name = image_data.name
                media.deleted = False
                media.deleted_at = None
                media.save()
                business.images.set(media)

        return instance

class PostListSerializer(serializers.ModelSerializer):
    Media = serializers.SerializerMethodField('get_Media')

    class Meta:
        model = Post
        fields = '__all__'



    def get_Media(self, obj):
        data = {}
        serializer_context = {'request': self.context.get('request')}
        media_data = PostImage.objects.filter(PostImages=obj)
        serializer = PostMediaSerializer(media_data, many=True, context=serializer_context)
        try:
            return serializer.data
        except:
            return data


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'
