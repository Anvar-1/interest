from django.conf import settings
from django.db import models

class Interest(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    interests = models.ManyToManyField(Interest, blank=True, related_name='video_interests')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='video_user_profile')
    interests = models.ManyToManyField(Interest, blank=True, related_name='video_user_profiles')

    def __str__(self):
        return self.user.username



class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/')
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_likes_count(self):
        return self.likes.count()  # Postga berilgan like'lar soni

    def get_likes_users(self):
        return [like.user.username for like in self.likes.all()]  # Like bergan foydalanuvchilar ro'yxati

    def get_comments_count(self):
        return self.comments.count()  # Postga qoldirilgan izohlar soni

    def get_comments(self):
        return [(comment.user.username, comment.content) for comment in self.comments.all()]  # Izohlar ro'yxati


class SearchHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.query} at {self.created_at}"