from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


class Contact(models.Model):
    first_name = models.CharField(_("First Name"), max_length=255)
    last_name = models.CharField(_("Last Name"), max_length=255)
    email = models.EmailField(_("Email"), max_length=512)
    phone = PhoneNumberField(null=True, blank=True)
    message = models.TextField(_("Message"))
    subscribe = models.BooleanField(_("Subscribe"), default=True)
