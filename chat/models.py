from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



# Create your models here.


class chat(models.Model):
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name="sender_user")
    reciver=models.ForeignKey(User,on_delete=models.CASCADE,related_name="reciver_user")
    

    def __str__(self):
        return f'chat between {self.sender} and {self.reciver}'
    


class message(models.Model):
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name="sender_message")
    reciver=models.ForeignKey(User,on_delete=models.CASCADE,related_name="reciver_message")
    cht=models.ForeignKey(chat,on_delete=models.CASCADE)
    mess=models.TextField()
    image=models.ImageField(upload_to='message-folder', blank=True, null=True)
    date=models.DateTimeField(default=timezone.now)
    
    
    def __str__(self):
        return f'message from {self.sender} to {self.reciver}'
    
