from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_admin = True
        user.user_type = 4
        user.save()
        return user



class User(AbstractBaseUser):
    USER_TYPE_CHOICES = (
        (1, 'None'),
        (2, 'Support'),
        (3, 'Sales'),
        (4, 'Admin'),
    )
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=100, unique=True)
    mobile = models.CharField(max_length=20)
    date_created = models.DateTimeField(default=datetime.now)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES,default=1,verbose_name="Type d'utilisateur")
    is_active = models.BooleanField(default=True,verbose_name="Actif")
    is_staff = models.BooleanField(default=False,verbose_name="Staff")
    is_admin = models.BooleanField(default=False,verbose_name='Admin')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    objects = UserManager()
