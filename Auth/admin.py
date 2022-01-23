import string
from random import random

from django.contrib import admin
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.admin import UserAdmin
from Auth.models import CustomUser,Otp,RefreshToke
# Register your models here.

# which acts a bit like a singleton
class EmployeeInline(admin.StackedInline):
    model = CustomUser
    can_delete = False
    verbose_name_plural = 'employee'

# Define a new User admin
class UserAdmin(BaseUserManager):
    inlines = (EmployeeInline,)

admin.site.register(CustomUser)
admin.site.register(Otp)
admin.site.register(RefreshToke)

