from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from epoqueart import settings

from django.utils.translation import gettext_lazy as _

import os
from uuid import uuid4


def wrapper(instance, filename):
    ext = filename.split('.')[-1]
    return 'images/userphotos/avatars/{}.{}'.format(uuid4().hex, ext)


class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    job = models.CharField(_('job'), max_length=255, default="Painter")
    avatar = models.ImageField(_('avatar'), upload_to=wrapper)
    is_painter = models.BooleanField(
        _('painter status'),
        default=False,
        help_text=_('Determines if the user can add their own paintings to the gallery.'),
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
