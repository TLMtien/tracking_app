from django.db import models
from django.db.models.enums import Choices
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# Create your models here.

TIGER_TP= 'tigerTP'
TIGER_FA= 'tigerFA'
TIGER_HZA= 'tigerHZA'
STRONGBOW = 'strongbow'
HEINEKEN ='heineken'
BIVINA = 'bivina'
LARUE = 'larue'

CHOICES_brand = [
    (TIGER_TP, 'TigerTP'),
    (TIGER_FA, 'TigerFA'),
    (TIGER_HZA, 'TigerHZA'),
    (STRONGBOW,'Strongbow Festive'),
    (HEINEKEN,'Heineken Festive'),
    (BIVINA,'Bivina Festive'),
    (LARUE,'larue Festive'),
]

class SalePerson(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    brand = models.CharField(choices = CHOICES_brand , default = HEINEKEN, max_length=200)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    province = models.CharField(max_length=200, null=True, blank=True)
    outlet = models.CharField(max_length=200, null=True, blank=True)
    joined = models.DateTimeField("Date Joined", auto_now_add=True)

    def __str__(self):
        return self.user.user_name
    
class HVN(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    brand = models.CharField(choices = CHOICES_brand , default = HEINEKEN, max_length=200)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    joined = models.DateTimeField("Date Joined", auto_now_add=True)

    def __str__(self):
        return self.user.user_name

class HVN_vip(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    joined = models.DateTimeField("Date Joined", auto_now_add=True)

    def __str__(self):
        return self.user.user_name


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, user_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(user_name,  password, **other_fields)

    def create_user(self, user_name,  password, **other_fields):
        
        user = self.model(user_name=user_name, **other_fields)
        user.set_password(password)
        user.save()
        return user
        
    
class NewUser(AbstractBaseUser, PermissionsMixin):

    user_name = models.CharField(max_length=150, unique=True)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_('about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    is_salePerson = models.BooleanField(default=False)
    is_HVN = models.BooleanField(default=False)
    is_HVNVip = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'user_name'
    

    def __str__(self):
        return self.user_name