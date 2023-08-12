from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver



class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.id} - {self.username}"

class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='postowner')
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    content = models.TextField()

    def __str__(self):
        return f" {self.id}: {self.owner} posted {self.content}"
    

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likedpost', blank=True, null=True )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="personwholiked", blank=True, null=True)

    def __str__(self):
        return f"user:{self.user} LIKED post: {self.post.content} "


class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers", default=False)
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following", default=False)

    def __str__(self):
        return f"{self.follower} is following {self.user}"
    
    class Meta:
        unique_together = ['user', 'follower']
    