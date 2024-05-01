from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    GENDER_CHOICE = (
        ("W", "Woman"),
        ("M", "Man"),
    )

    nickname = models.CharField(max_length=50, default='')
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1,choices=GENDER_CHOICE, default='M')

