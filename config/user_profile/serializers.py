from rest_framework import serializers
from .models import UserProfile, Interest

class UserProfileSerializer(serializers.ModelSerializer):
    interests = serializers.StringRelatedField(many=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'user_img', 'subscribers_count', 'videos_count', 'photos_count', 'interests']