from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


class Release(models.Model):
    year = models.IntegerField()
    
    def __str__(self):
        return str(self.year)
  
    
class WatchList(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='photos/watchlist')
    storyline = models.CharField(max_length=500,blank=True)
    avg_rating = models.FloatField(default=0)
    total_rating = models.IntegerField(default=0)
    length = models.IntegerField()
    release = models.ForeignKey(Release,on_delete=models.DO_NOTHING,blank=True)
    director = models.CharField(max_length=200)
    writer = models.CharField(max_length=200)
    stars = models.CharField(max_length=250)
    category = models.ManyToManyField(Category,related_name='genre_list')
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title


class Review(models.Model):
    reviewer = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    rating = models.IntegerField(choices=[(i,i) for i in range(1,6)])
    description = models.CharField(max_length=250)
    watchlist = models.ForeignKey(WatchList,on_delete=models.CASCADE,related_name='reviews')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Rating: {self.rating} -|- Movie: {self.watchlist.title}"