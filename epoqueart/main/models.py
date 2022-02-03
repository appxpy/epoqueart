from django.db import models
from accounts.models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
import datetime
import os
from uuid import uuid4


def wrapper(instance, filename):
    ext = filename.split(".")[-1]
    return "images/content/{}.{}".format(uuid4().hex, ext)


class Painting(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name=_("Author account")
    )
    name = models.CharField(
        _("Picture name"), max_length=512, default="Unnamed Painting"
    )
    image = models.ImageField(_("Painting"), upload_to=wrapper)
    description = models.TextField(_("Description"))
    price = models.FloatField(_("Price ($)"), default=0)
    date = models.DateField(_("Date"), default=now)

    # features
    is_offline_available = models.BooleanField(
        _("Availability in the offline store"),
        default=False,
        help_text=_("Determines if there is a painting in the store at the moment."),
    )

    is_nft = models.BooleanField(
        _("NFT"),
        default=False,
        help_text=_("Determines if an NFT token is linked to a painting."),
    )

    def __str__(self):
        return f"{self.name} ({self.author.first_name} {self.author.last_name})"
