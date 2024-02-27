from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class twitts(models.Model):
    name=models.ForeignKey(User,on_delete=models.CASCADE)
    twitt=models.TextField()
    date=models.DateTimeField(default=timezone.now)
    
    
    def __str__(self):
        return self.twitt
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})