from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, is_active=True, is_staff=False, is_superuser=False):
        if not phone:
            raise ValueError('Telefon raqamini kiriting')
        user = self.model(phone=phone, is_active=is_active, is_staff=is_staff, is_superuser=is_superuser)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone, password=None, is_staff=True, is_superuser=True):
        return self.create_user(phone=phone, password=password, is_staff=is_staff, is_superuser=is_superuser)
    

class CustomUser(AbstractBaseUser):
    phone = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=20)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name'] 
    
    def __str__(self):
        return self.phone
    def format(self):
        return {
            'phone':self.phone,
            'name':self.name,
            'is_active':self.is_active,
            'is_staff':self.is_staff,
            'is_superuser':self.is_superuser
        }