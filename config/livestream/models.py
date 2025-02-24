from django.db import models
from django.conf import settings

class LiveStream(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='live_stream')
    title = models.CharField(max_length=255)
    stream_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
