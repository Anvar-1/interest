from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Video, Interest, UserProfile, Post, SearchHistory
from .serializers import VideoSerializer, InterestSerializer, UserProfileSerializer, PostSerializer
from ..users.serializers import UserSerializer

User = get_user_model()

class SearchView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q', None)
        if not query:
            return Response({"error": "Qidirish so'rovi berilmagan."}, status=status.HTTP_400_BAD_REQUEST)

        # Video postlarni qidirish
        posts = Post.objects.filter(video__icontains=query)
        users = User.objects.filter(username__icontains=query)

        # Qidirish tarixini saqlash
        SearchHistory.objects.create(user=request.user, query=query)

        # Natijalarni tayyorlash
        post_serializer = PostSerializer(posts, many=True)
        user_serializer = UserSerializer(users, many=True)

        if not posts.exists() and not users.exists():
            return Response({"message": "User yoki video topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "posts": post_serializer.data,
            "users": user_serializer.data,
            "message": "Qidiruv natijalari."
        })

class DeleteSearchHistoryView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        query = request.query_params.get('q', None)

        if not query:
            return Response({"error": "Qidirish so'rovi berilmagan."}, status=status.HTTP_400_BAD_REQUEST)

        # Qidirish tarixini o'chirish
        deleted_count = SearchHistory.objects.filter(user=request.user, query=query).delete()

        if deleted_count == 0:
            return Response({"message": "O'chirish uchun yozuv topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Qidirish tarixi o'chirildi."}, status=status.HTTP_204_NO_CONTENT)

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
        if instance.user == self.request.user:
            instance.delete()
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

class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = self.get_serializer(post)

        # Post ma'lumotlarini olish
        data = serializer.data
        data['likes_count'] = post.get_likes_count()
        data['likes_users'] = post.get_likes_users()
        data['comments_count'] = post.get_comments_count()
        data['comments'] = post.get_comments()

        return Response(data)

class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        video = self.request.FILES.get('video')
        if video and video.size > 100 * 1024 * 1024:  # 100 MB
            return Response({"error": "Video o'lchami 100 MB dan oshmasligi kerak."}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=self.request.user)