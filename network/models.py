from django.contrib.auth.models import AbstractUser
from django.db import models



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
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likedpost' )
    liked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}: {self.post.owner} {self.post.content} {self.liked}"


class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    follower = models.ManyToManyField(User, blank=True, null=True, related_name="followers")

    def __str__(self):
        return f"{self.user} has {self.follower.count()} followers"


class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userwhoisfollowing")
    following = models.ManyToManyField(User, blank=True, null=True, related_name="userfollowings")

    def __str__(self):
        return f"{self.user} is following {self.following.count()} profiles"



