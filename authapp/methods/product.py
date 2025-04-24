from django.db import models
from authapp.models import CustomUser
class Category(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name
    

class Post(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    short_desc=models.CharField(max_length=250)
    