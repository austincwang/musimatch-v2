from django.db import models

# Create your models here.
class Game(models.Model):
    artist = models.CharField(max_length=25)
    song = models.CharField(max_length=50)
    timeperiod = models.DateField()
    date = models.DateTimeField(auto_now_add=True)

