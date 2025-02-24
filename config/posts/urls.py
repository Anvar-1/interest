from django.urls import path
from .views import PostListCreateView, PostDetailView, CommentCreateView

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:post_id>/comments/', CommentCreateView.as_view(), name='comment-create'),
]