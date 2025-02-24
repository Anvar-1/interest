from rest_framework import generics
from .models import Post, Comment
from .serializers import CommentSerializer
from ..users import serializers


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']  # URL dan post_id ni olish
        post = Post.objects.get(id=post_id)  # Berilgan post ID'sini olish
        serializer.save(post=post)  # Kommentni saqlash



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'content', 'created_at']  # 'post' maydonini qo'shish
        read_only_fields = ['post']  # 'post' maydoni faqat server tomonidan beriladi




class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'content', 'created_at', 'likes', 'photo', 'video', 'comments']