from django.conf import settings
from django.db import models
from config.videoshare.models import Interest

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_profile'
    )
    interests = models.ManyToManyField(Interest, blank=True, related_name='general_user_profiles')
    user_img = models.ImageField(upload_to='profiles/', blank=True, null=True)
    subscribers_count = models.PositiveIntegerField(default=0)
    videos_count = models.PositiveIntegerField(default=0)
    photos_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username