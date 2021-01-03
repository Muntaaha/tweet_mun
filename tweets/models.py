from django.db import models
from django.conf import settings
import random

User = settings.AUTH_USER_MODEL

# Create your models here.

class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweets", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Tweets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    likes = models.ManyToManyField(User, related_name='tweet_user', blank=True, through=TweetLike)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        ordering = ['-id']
    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 200)
        }