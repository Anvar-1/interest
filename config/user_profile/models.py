from django.conf import settings
from django.db import models

class Interest(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='subscribers', on_delete=models.CASCADE)
    subscribed_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='subscriptions', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('subscriber', 'subscribed_to')

    def __str__(self):
        return f"{self.subscriber.username} -> {self.subscribed_to.username}"

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_profile')
    interests = models.ManyToManyField(Interest, blank=True, related_name='general_user_profiles')
    user_img = models.ImageField(upload_to='profiles/', blank=True, null=True)
    subscribers_count = models.PositiveIntegerField(default=0)
    videos_count = models.PositiveIntegerField(default=0)
    photos_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username

    def update_subscribers_count(self):
        self.subscribers_count = self.user.subscribers.count()
        self.save()