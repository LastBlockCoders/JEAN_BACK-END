from django.db import models
from django.contrib.auth.models import AbstractUser,  PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError(_("Email should be provided"))

        if not phone_number:
            raise ValueError(_("Phone number should be provided"))

        email = self.normalize_email(email)

        user = self.model(email=email, username=username,
                          phone_number=phone_number, **extra_fields)
        user.set_password(password)

        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to have is_staff set to True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_superuser set to True")

        if extra_fields.get("is_active") is not True:
            raise ValueError(_("Superuser should have is_active as True"))

        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    email = models.CharField(max_length=80, unique=True)
    username = models.CharField(max_length=50)
    phone_number = PhoneNumberField(null=False, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_secretary = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=False)
    gender = models.CharField(max_length=6)

    objects = CustomUserManager()
    # This will treat the email as the username for client users
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "phone_number", "date_of_birth", "gender"]

    def __str__(self):
        return self.email
