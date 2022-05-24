from sqlite3 import Timestamp
from django.contrib.auth.models import AbstractUser
from django.db import models


    
class User(AbstractUser):
    pass

class Post(models.Model):
    body = models.TextField(blank=True)
    likes = models.ManyToManyField("User", on_delete = models.cascade, related_name = "liked_posts")
    timestamp = models.DateTimeField(auto_now_add= True)
    edited_on = models.DateTimeField (auto_now = True)

