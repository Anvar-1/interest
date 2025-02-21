from django.urls import path
from .views import VideoListCreateView, VideoDetailView, InterestListCreateView, UserProfileCreateView, RecommendationsView

urlpatterns = [
    path('videos/', VideoListCreateView.as_view(), name='video-list-create'),
    path('videos/<int:pk>/', VideoDetailView.as_view(), name='video-detail'),
    path('interests/', InterestListCreateView.as_view(), name='interest-list-create'),
    path('user/profile/', UserProfileCreateView.as_view(), name='user-profile-create'),
    path('recommendations/<int:user_id>/', RecommendationsView.as_view(), name='recommendations'),
]
