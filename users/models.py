import random

from django.contrib.auth.models import AbstractUser
from django.db import models





class User(AbstractUser):
    username = models.CharField(max_length=24, null=False, unique=True)
    password = models.CharField(max_length=24, null=False)
    password_confirm = models.CharField(max_length=64, null=False)
    net_name = models.CharField(default=str(random.randint(100000, 200000)), null=True, max_length=24)
    sex = models.IntegerField(default=2, null=False)
    avatar = models.ImageField(blank=True, null=True)
    birthday = models.DateField(null=True)
    college = models.CharField(null=True, max_length=10)
    major = models.CharField(null=True, max_length=10)
    self_describe = models.CharField(null=True, max_length=64)

    class Meta:
        db_table = 'users'
        verbose_name = '用户表'





