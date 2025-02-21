from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from .models import Video, Interest, UserProfile
from .serializers import VideoSerializer, InterestSerializer, UserProfileSerializer

class VideoListCreateView(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class VideoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.user == self.request.user:  # Foydalanuvchi video egasi bo'lsa
            instance.delete()  # Videoni o'chirish
        else:
            raise PermissionDenied("Siz ushbu videoni o'chirish huquqiga ega emassiz.")

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

