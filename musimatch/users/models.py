from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    description = models.TextField(max_length=200, default='I\'m using Musimatch!', blank=True)
    pfp = models.ImageField(default='default_pfp.jpg', blank=True, null=True, upload_to='images/')

    def __str__(self):
        return self.username

