import string
import random

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

# Create your models here.
class MyUserAdmin(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
        email = models.EmailField(
            verbose_name='email address',
            max_length=255,
            unique=True,
            error_messages={
                'unique': ("This email is already registered")
            }
        )
        name=models.CharField(max_length=99,null=True)
        is_active = models.BooleanField(default=False)
        is_admin = models.BooleanField(default=False)

        objects = MyUserAdmin()

        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = ['name']

        def __str__(self):
            return self.name

        def has_perm(self, perm, obj=None):
            "Does the user have a specific permission?"
            # Simplest possible answer: Yes, always
            return True

        def has_module_perms(self, app_label):
            "Does the user have permissions to view the app `app_label`?"
            # Simplest possible answer: Yes, always
            return True

        @property
        def is_staff(self):
            "Is the user a member of staff?"
            # Simplest possible answer: All admins are staff
            return self.is_admin

class RefreshToke(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    refreshToken=models.CharField(blank=False,null=False,max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

def generateOtp():
    return ''.join(random.choice(string.digits) for x in range(6))

class Otp(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    otp = models.CharField(max_length=6, default=''.join(random.choice(string.digits) for x in range(6)), unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    class Meta:
        ordering = ['created_at']


