from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _

from .managers import UserManager
from django.utils import timezone
# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique= True)
    phone = models.CharField(_('phone number'),unique= True, max_length= 15)
    first_name= models.CharField(_('first name'), max_length= 30, blank= True)
    last_name= models.CharField(_('last name'), max_length= 30, blank= True)
    date_joined= models.DateTimeField(_('date joined'), auto_now_add= True)
    is_staff= models.BooleanField(_('staff'), default= False)
    is_admin= models.BooleanField(_('admin'), default= False)
    is_superuser= models.BooleanField(_('superuser'), default= False)
    is_active= models.BooleanField(_('active'), default= False)
    is_payment= models.BooleanField(_('payment'),default= False)
    

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']


    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    
    def __str__(self) -> str:
        return self.email

class Otp(models.Model):
    code= models.CharField(max_length=6)
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    expiry_date= models.DateTimeField()

    def __str__(self) -> str:
        return f'{self.code} >>> {self.user.email}'

    def is_expired(self):
        return timezone.now() > self.expiry_date

class Forgot(models.Model):
    email_forgot = models.EmailField(_('email address'))