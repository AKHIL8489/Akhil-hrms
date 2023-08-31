from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    emplyeeIdentficationCode = models.CharField(max_length=50)
    joining_date = models.DateField(default='')
    phone = models.CharField(max_length=15,default='')
    department = models.CharField(max_length=255,default='')
    designation = models.CharField(max_length=255,default='')

    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }