from email.policy import default
from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
import uuid

User = get_user_model()

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile-images', default='blankprofile.jpg')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=150)
    image = models.ImageField(upload_to='post-images')
    caption = models.TextField()
    created_at = models.DateTimeField(default = datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user

class Likepost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=150)

    def __str__(self):
        return self.username

class Followercount(models.Model):
    follower = models.CharField(max_length=150)
    user = models.CharField(max_length=150)

    def __str__(self):
        return self.user