from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, BaseUserManager


class UserAccountManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, address, phone_number, password, status='ACTIVE', **other_fields):
        email = self.normalize_email(email)
        user = self.model(username=username, first_name=first_name, last_name=last_name, email=email, address=address,
                          phone_number=phone_number, status=status, password=password, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, first_name, last_name, email, address, phone_number, password, status='ACTIVE', **other_fields):
        return self.create_user(username, first_name, last_name, email, address, phone_number, password, status, **other_fields)


class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    address = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=20)
    status = models.CharField(max_length=10, default='ACTIVE')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'address', 'phone_number', 'username']

    objects = UserAccountManager()

    def __str__(self):
        return self.username + self.email
