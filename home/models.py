# from django.db import models

# class Medicine(models.Model):
#     name = models.CharField(max_length=100)
#     brand = models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     expiration_date = models.DateField()
#     dosage = models.CharField(max_length=50)
#     quantity = models.PositiveIntegerField()
#     usage_instructions = models.TextField()
#     side_effects = models.TextField(blank=True, null=True)
#     storage_conditions = models.CharField(max_length=200, blank=True, null=True)
#     image = models.ImageField(upload_to="media/", null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     objects = models.Manager()

#     def __str__(self):
#         return f"{self.brand} - {self.name} ({self.dosage})"

