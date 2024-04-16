from datetime import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models

# models: User, Post, Like, Follow

class User(AbstractUser):
    profileImg = models.URLField(max_length=1050, default="", null = True, blank=True)
    coverImg = models.URLField(max_length=1050, default="", null = True, blank=True)
    userLikes = models.ManyToManyField('Like', related_name="userLikes", blank=True)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="", related_name="posts")
    post = models.CharField(max_length=620, default="")
    timestamp = models.DateTimeField(blank=True)
    likes = models.ManyToManyField('Like', related_name="postLikes", blank=True)

    def __str__(self):
        return f"{self.id}:{self.post}:{self.user}"      
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default="")

    def __str__(self):
        return f"{self.id}:{self.user}:{self.post.id}"

    

class Following(models.Model):
    follower = models.ForeignKey(User,  on_delete=models.CASCADE, default="", related_name="userFollowers")
    followingOthers = models.ForeignKey(User, on_delete=models.CASCADE, default="", related_name="followingOthers")

    def __str__(self):
        return f"{self.follower} following: {self.followingOthers}"
    
    def get_user_following_posts(self):
        return self.followingOthers.posts.all()