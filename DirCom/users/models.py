from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import connection

from persons.models import Person


class UserAccountManager(BaseUserManager):
    def create_user(self, username, email, password, person_fk, status='ACTIVE', **other_fields):
        email = self.normalize_email(email)
        user = self.model(username=username, status=status, person_fk=person_fk,  password=password, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, person_fk, status='ACTIVE',  **other_fields):
        return self.create_user(username, email, password, status, person_fk, **other_fields)


class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    person_fk = models.ForeignKey(Person, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default='ACTIVE')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'status', 'person_fk']

    objects = UserAccountManager()

    ''' @staticmethod
    def list_users(status_filter):
        list_query = " SELECT id, username, first_name, last_name, email, phone_number, status FROM users_user "
        order_by = " ORDER BY id desc "
        if status_filter is not None:
            filter = " WHERE status = %s "
            final_query = list_query + filter + order_by
            with connection.cursor(final_query, [status_filter]) as cursor:
                cursor.execute()
                row = cursor.fetchall()
            return row
        else:
            final_query = list_query + order_by
            with connection.cursor() as cursor:
                cursor.execute(final_query, [])
                row = cursor.fetchall()
            return row'''

    @staticmethod
    def status_change(status, pk):
        with connection.cursor() as cursor:
            cursor.execute("UPDATE users_user SET status = %s WHERE id = %s RETURNING id", [status, pk])
            row = cursor.fetchone()
        return row

    def __str__(self):
        return self.username + self.email



class UserClass():
    def __init__(self):
        pass
