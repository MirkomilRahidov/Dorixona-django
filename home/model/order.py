from django.db import models
from authapp.models import CustomUser
from .card import Card
class Order(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete= models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.user} - {self.card}"
    