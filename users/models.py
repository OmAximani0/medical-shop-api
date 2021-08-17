from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext as _

# Manager For Custom User
class CustomerUserManager(BaseUserManager):
    
    def create_user(self, password,**extra_fields):
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))       

        return self.create_user(password,**extra_fields)

# Models

class Users(AbstractUser):
    objects = CustomerUserManager()
    first_name = None
    last_name = None
    username = None
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=200)
    user_email = models.EmailField(unique=True)
    role_name = models.CharField(max_length=50, default='Customer', null=False)

    USERNAME_FIELD = 'user_email'

    REQUIRED_FIELDS = ['user_name', 'password'] 

    class Meta:
        db_table = 'users'
        verbose_name_plural = "users"

