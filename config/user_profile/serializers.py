from rest_framework import serializers
from .models import UserProfile, Interest, Subscription

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id', 'name']

class UserProfileSerializer(serializers.ModelSerializer):
    interests = InterestSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'user_img', 'subscribers_count', 'videos_count', 'photos_count', 'interests']

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'subscriber', 'subscribed_to', 'created_at']
        read_only_fields = ['subscriber', 'created_at']