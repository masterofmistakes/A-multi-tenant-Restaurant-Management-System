from django.db import models
from restaurants.models import Restaurant
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserRole(models.TextChoices):
    SUPERADMIN = 'super_admin', 'Super_Admin'
    ADMIN = 'admin', 'Admin'
    WAITER = 'waiter', 'Offitsiant'
    CHEF = 'chef', 'Aspaz'
    SKLADCHIK = 'skladchik', 'Skladchik'
    CLIENT = 'client', 'Klent'

class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("Enter your phone number...")
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', UserRole.SUPERADMIN)
        return self.create_user(phone, password, **extra_fields)
    
class User(AbstractUser):
    username = None
    fullname = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    avatar = models.ImageField(upload_to='users/', null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, related_name='users', null=True, blank=True)
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.CLIENT)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone