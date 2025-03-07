from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class WatchList(models.Model):
    titile = models.CharField(max_length=100)
    description = models.TextField()
    platform  = models.ForeignKey("StreamPlatform", on_delete=models.CASCADE, related_name="watchlist")
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.titile

class StreamPlatform(models.Model):
    name = models.CharField(max_length=30)
    about = models.TextField()
    website = models.URLField(max_length=30)
    
    def __str__(self):
        return self.name
    
class Review(models.Model):
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name="reviews")
    
    def __str__(self):
        return str(self.rating) + " | " + self.watchlist.titile