import decimal
from django.db import models
from authapp.models import CustomUser
from .products import Medicine
class Card(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    post = models.ForeignKey(Medicine, on_delete= models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        self.price = float(self.card.price) * float(self.quantity)
        super(Card, self).save(*args, **kwargs)
    def __str__(self):
        return f"{self.user}-{self.quantity}"