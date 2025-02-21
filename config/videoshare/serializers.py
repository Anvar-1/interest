from rest_framework import serializers
from .models import Video, Interest, UserProfile

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id', 'name']

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'video_file', 'thumbnail', 'interests', 'user', 'uploaded_at']

class UserProfileSerializer(serializers.ModelSerializer):
    interests = InterestSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'interests']
