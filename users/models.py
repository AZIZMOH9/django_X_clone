from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.

class profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(default='default.jpg', upload_to='profile_pics')
    
    
    def __str__(self):
        return f'{self.user.username} Profile'
    

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.image.path)


class follow(models.Model):
    follower=models.ForeignKey(User,on_delete=models.CASCADE,related_name="follower")
    followed=models.ForeignKey(User,on_delete=models.CASCADE,related_name="followed")

    def __str__(self):
        return "following table"