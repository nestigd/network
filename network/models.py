from sqlite3 import Timestamp
from django.contrib.auth.models import AbstractUser
from django.db import models


    
class User(AbstractUser):
    pass

class Post(models.Model):
    poster = models.ForeignKey("User", on_delete = models.CASCADE, related_name = "posts")
    body = models.TextField(blank=True)
    likes = models.ManyToManyField("User", related_name = "liked_posts", default=0)
    timestamp = models.DateTimeField(auto_now_add= True)
    
    def __str__ (self):
        return f"{self.id} - {self.poster.username} - {self.body[:8]}"