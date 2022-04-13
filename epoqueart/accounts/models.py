from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from epoqueart import settings

from django.utils.translation import gettext_lazy as _

import os
from uuid import uuid4


def wrapper(instance, filename):
    ext = filename.split(".")[-1]
    return "images/userphotos/avatars/{}.{}".format(uuid4().hex, ext)


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    OWNER = 1
    ADMIN = 2
    EMPLOYEE = 3
    USER = 4
    NOTACTIVE = 5

    ROLE_CHOICES = (
        (
            "Administrative",
            (
                ("Owner", _("Owner")),
                ("Administrator", _("Administrator")),
                ("Employee", _("Employee")),
            ),
        ),
        (
            "Non-Administrative",
            (
                ("User", _("User")),
                ("Not Active", _("Not Active")),
            ),
        ),
    )

    username = None
    email = models.EmailField(_("Email"), unique=True)
    avatar = models.ImageField(_("Avatar"), upload_to=wrapper, null=True)
    role = models.CharField(
        _("Role"), max_length=64, choices=ROLE_CHOICES, default="User"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
