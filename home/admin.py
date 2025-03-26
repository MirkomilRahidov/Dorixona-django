from django.contrib import admin
from .models import Medicine
admin.site.register(Medicine)
class YourModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'text')
# Register your models here.
