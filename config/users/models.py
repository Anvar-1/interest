from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

class UserRoleManager(BaseUserManager):

    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("Telefon raqam kiritilishi shart")
        extra_fields.setdefault("is_active", True)
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser uchun `is_staff=True` bo‘lishi shart")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser uchun `is_superuser=True` bo‘lishi shart")
        return self.create_user(phone, password, **extra_fields)


class User(AbstractUser):
    GENDER_CHOICES = [
        ('male', 'Erkak'),
        ('female', 'Ayol'),
        ('other', 'Boshqa'),
    ]

    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, unique=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    interests = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserRoleManager()
    username = None

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['full_name']

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }