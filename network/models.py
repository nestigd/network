from django.contrib.auth.models import AbstractUser
from django.db import models


    
class User(AbstractUser):
    pass

class Post(models.Model):
    body = models.TextField(blank=True)
    likes = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add= True)
    

