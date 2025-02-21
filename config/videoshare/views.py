from rest_framework import generics
from .models import Video, Interest, UserProfile
from .serializers import VideoSerializer, InterestSerializer, UserProfileSerializer

class VideoListCreateView(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

class VideoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

class InterestListCreateView(generics.ListCreateAPIView):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer

class UserProfileCreateView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class RecommendationsView(generics.ListAPIView):
    serializer_class = VideoSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user_profile = UserProfile.objects.get(user_id=user_id)
        return Video.objects.filter(interests__in=user_profile.interests.all()).distinct()

