from django.db import models

# Create your models here.
class WatchList(models.Model):
    titile = models.CharField(max_length=100)
    description = models.TextField()
    platform  = models.ForeignKey("StreamPlatform", on_delete=models.CASCADE, related_name="watchlist")
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.titile

class StreamPlatform(models.Model):
    name = models.CharField(max_length=30)
    about = models.TextField()
    website = models.URLField(max_length=30)
    
    def __str__(self):
        return self.name