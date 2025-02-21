from requests import Response
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile, Subscription
from .serializers import UserProfileSerializer, SubscriptionSerializer


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.userprofile


class SubscribeView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(subscriber=self.request.user)
        # Obunachilar sonini yangilash
        subscribed_user_profile = self.request.user.user_profile
        subscribed_user_profile.update_subscribers_count()
        return Response({"message": "Successfully subscribed!"})

class SubscriberListView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(subscribed_to=self.request.user)


    ####  obunachini uchirish #####
class UnsubscribeView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Subscription.objects.get(subscriber=self.request.user, subscribed_to=self.kwargs['user_id'])



