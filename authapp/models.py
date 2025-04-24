
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        if not phone:
            raise ValueError("Foydalanuvchida telefon bo'lishi shart")
        user = self.model(phone=phone)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password):
        user = self.create_user(phone, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    phone = models.CharField(max_length=13, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    phone = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=20)
    email = models.EmailField(unique=True, null=True, blank=True)  

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name', 'email'] 
    def __str__(self):
        return self.phone

    def format(self):
        return {
            'phone': self.phone,
            'name': self.name,
            'email': self.email,
            'is_active': self.is_active,
            'is_staff': self.is_staff,
            'is_superuser': self.is_superuser
        }


class OTP(models.Model):
    phone = models.CharField(max_length=12)
    key = models.CharField(max_length=100)
    created= models.DateTimeField(auto_now_add=True)
    is_expire = models.BooleanField(default=False)
    is_conf = models.BooleanField(default=True)
    tried = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.tried >= 3:
            self.is_expire = True
        super(OTP, self).save(*args, **kwargs)
