from django.contrib import admin
from home.model.products import Medicine
admin.site.register(Medicine)
class YourModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'text')
# Register your models here.
