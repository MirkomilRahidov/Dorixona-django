from django.db import models
from authapp.models import CustomUser
from authapp.methods.product import Post
class Order(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete= models.CASCADE)
    status = models.BooleanField(default=False)
    