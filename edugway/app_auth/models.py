import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField('Username', unique=True, max_length=40)
    first_name = models.CharField('Username', max_length=60)
    last_name = models.CharField('Username', max_length=60)
    email = models.EmailField('Email', unique=True, max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = BaseUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', ]

    def __str__(self):
        return self.get_full_name() + '(' + self.email + ')'
