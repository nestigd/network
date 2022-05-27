from sqlite3 import Timestamp
from django.contrib.auth.models import AbstractUser
from django.db import models


    
class User(AbstractUser):
    pass

class Post(models.Model):
    poster = models.ForeignKey("User", on_delete = models.CASCADE, related_name = "posts")
    body = models.TextField(blank=True)
    likes = models.ManyToManyField("User", related_name = "liked_posts", blank=True)
    timestamp = models.DateTimeField(auto_now_add= True)
    edited_on = models.DateTimeField (auto_now = True)
    
    def __str__ (self):
        return f"{self.id} - {self.poster.username} - {self.body[:8]}"

    def serialize(self):
        return {
            "id" : self.id,
            "poster" : self.poster.username,
            "body" : self.body,
            "likes" : self.likes.all().count(),
            "timestamp": self.timestamp,
            "edited_on" : self.edited_on,
        }

    def is_valid_post (self):
        return self.body != ""  