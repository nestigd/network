from email.quoprimime import body_length
from sqlite3 import Timestamp
from django.contrib.auth.models import AbstractUser
from django.db import models


    
class User(AbstractUser):
    def __str__ (self):
        return f"{self.id} - {self.username}"

class Post(models.Model):
    poster = models.ForeignKey("User", on_delete = models.CASCADE, related_name = "posts")
    body = models.TextField(blank=True, max_length=255)
    timestamp = models.DateTimeField(auto_now_add= True)
    edited_on = models.DateTimeField (auto_now = True)
    
    def __str__ (self):
        return f"{self.id} - {self.poster.username} - {self.body[:8]}"

    # the serializer takes an argumen USER so it can check if the post was liked by the user or not
    def serialize(self, user):
        return {
            "id" : self.id,
            "poster" : self.poster.username,
            "poster_id" : self.poster.id,
            "body" : self.body,
            "timestamp": self.timestamp,
            "edited_on" : self.edited_on,
            "liked" : (Like.objects.filter(post = self, user = user).count() > 0)
        }

    def is_valid_post (self):
        return self.body != "" and len(self.body) < 256

class Following(models.Model):
    follower= models.ForeignKey("User", on_delete = models.CASCADE, related_name = "following")
    followed= models.ForeignKey("User", on_delete = models.CASCADE, related_name= "followers")
    
    def __str__(self):
        return f"{self.follower} -> {self.followed}"
    
class Like(models.Model):
    post= models.ForeignKey("Post", on_delete= models.CASCADE, related_name = "likes")
    user= models.ForeignKey("User", on_delete= models.CASCADE, related_name= "likes")
    
    def __str__(self):
        return f"{self.user} -> {self.post} by {self.post.poster.username}"    
        