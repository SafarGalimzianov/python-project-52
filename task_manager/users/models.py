from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    '''
    id = models.AutoField(primary_key=True, default=1000)
    username = models.CharField(unique=True, default=1000)
    first_name = models.CharField(default=1000)
    last_name = models.CharField(default=1000)
    password = models.CharField(default=1000)
    '''

    def __str__(self):
        return f"{self.first_name} {self.last_name}"