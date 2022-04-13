import datetime
import os
from django.db import models
from django.forms import ValidationError
from accounts.models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.utils import timezone
from uuid import uuid4


def wrapper(instance, filename):
    ext = filename.split(".")[-1]
    return "images/content/{}.{}".format(uuid4().hex, ext)


class Country(models.Model):
    country = models.CharField(_("Country"), max_length=255)

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")

    def __str__(self):
        return self.country


class City(models.Model):
    city_name = models.CharField(_("City name"), max_length=255)
    postal_code = models.CharField(_("Postal code"), max_length=32)
    country = models.ForeignKey(
        Country, verbose_name=_("Country"), on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")

    def __str__(self):
        return self.city_name


class Currency(models.Model):
    country = models.ForeignKey(
        Country, on_delete=models.PROTECT, verbose_name=_("Country")
    )
    currency_name = models.CharField(_("Currency name"), max_length=255)
    currency_short = models.CharField(
        _("Currency short name"),
        max_length=10,
        help_text=_("Currency short name, e.g. 'EUR'"),
    )
    currency_symbol = models.CharField(
        _("Currency symbol"), max_length=3, help_text="Currency symbol, e.g. '€'"
    )

    class Meta:
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")

    def __str__(self):
        return self.currency_name


class Gallery(models.Model):
    gallery_name = models.CharField(
        _("Gallery name"), max_length=255, help_text=_("Name of physical gallery.")
    )
    gallery_address = models.CharField(_("Gallery address"), max_length=512)
    gallery_description = models.TextField(
        _("Gallery description"), max_length=512, blank=True
    )
    city = models.ForeignKey(City, verbose_name=_("City"), on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.gallery_name} - {self.gallery_address}"

    class Meta:
        verbose_name = _("Gallery")
        verbose_name_plural = _("Galleries")


class Author(models.Model):
    preview_image = models.ImageField(
        _("Author preview image"),
        upload_to=wrapper,
        help_text=_("This image will be shown at author preview page."),
    )
    image = models.ImageField(
        _("Author image"),
        upload_to=wrapper,
        help_text=_("This image will be shown at author page."),
    )
    name = models.CharField(_("Full name"), max_length=255, unique=True)
    qualification = models.CharField(
        _("Qualification"),
        max_length=255,
        help_text=_("Qualification of author, e.g. 'Surrealist master'"),
    )
    description = models.TextField(_("Description"))
    slug = models.SlugField(_("Slug"), unique=True, editable=False, null=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")

    def get_personal_url(self):
        return self.slug or slugify(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Author, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if os.path.isfile(self.preview_image.path):
            os.remove(self.preview_image.path)

        if os.path.isfile(self.image.path):
            os.remove(self.image.path)

        super(Author, self).delete(*args, **kwargs)


class Artwork_Type(models.Model):
    artwork_type_name = models.CharField(
        _("Type"),
        max_length=255,
        unique=True,
        help_text=_("Type of artwork, e.g. 'Bust'"),
    )

    def __str__(self):
        return self.artwork_type_name

    class Meta:
        verbose_name = _("Artwork Type")
        verbose_name_plural = _("Artwork Type")


class Artwork_Status(models.Model):
    artwork_status_name = models.CharField(
        _("Status"),
        max_length=255,
        unique=True,
        help_text=_("Status of artwork, e.g. 'Sold' or 'Reserved'"),
    )
    artwork_is_available = models.BooleanField(
        _("Is Available"),
        default=True,
        help_text=_("Determines if artwork is available to customers."),
    )

    def __str__(self):
        return self.artwork_status_name

    class Meta:
        verbose_name = _("Artwork Status")
        verbose_name_plural = _("Artwork Status")


class Artwork(models.Model):
    title = models.CharField(
        _("Title"), max_length=255, help_text=_("Title of artwork.")
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.PROTECT,
        verbose_name=_("Author"),
        help_text=_("Author of artwork."),
    )
    date = models.DateField(
        _("Date"), null=True, help_text=_("Date of creation of artwork.")
    )

    image = models.ImageField(
        _("Image"), upload_to=wrapper, help_text=_("High-res image of artwork.")
    )

    description = models.TextField(
        _("Description"), help_text=_("Description of artwork.")
    )

    type = models.ForeignKey(
        Artwork_Type,
        on_delete=models.PROTECT,
        verbose_name=_("Type"),
        help_text=_("Type of artwork."),
    )

    width = models.PositiveIntegerField(
        _("Width"), help_text=_("Determines width of artwork."), null=True
    )

    height = models.PositiveIntegerField(
        _("Height"), help_text=_("Determines height of artwork."), null=True
    )

    MEASURE_CHOICES = (
        ("Inch", _("Inch")),
        ("Centimeters", _("Centimeters")),
    )

    measure = models.CharField(
        _("Measure unit"), choices=MEASURE_CHOICES, max_length=24
    )
    materials = models.CharField(
        _("Materials"), max_length=255, null=True, help_text=_("Materials of artwork.")
    )

    price = models.PositiveIntegerField(_("Price"), help_text=_("Price of artwork."))

    currency = models.ForeignKey(
        Currency,
        verbose_name=("Currency"),
        on_delete=models.PROTECT,
        help_text=_("Payment currency."),
    )

    is_nft_linked = models.BooleanField(
        _("Is NFT token linked?"),
        default=False,
        help_text=_("Determines if the token is linked to a physical object."),
    )

    location = models.ForeignKey(
        Gallery,
        verbose_name=_("Location"),
        on_delete=models.PROTECT,
        help_text=_("Physical location of artwork."),
    )
    status = models.ForeignKey(
        Artwork_Status,
        on_delete=models.PROTECT,
        verbose_name=_("Status"),
        help_text=_("Status of artwork."),
    )

    def get_size_cm(self):
        if self.measure == "Inch":
            return (int(round(self.width * 2.54, 0)), int(round(self.height * 2.54, 0)))
        if self.measure == "Centimeters":
            return (self.width, self.height)

    def get_size_inch(self):
        if self.measure == "Centimeters":
            return (int(round(self.width / 2.54, 0)), int(round(self.height / 2.54, 0)))
        if self.measure == "Inch":
            return (self.width, self.height)

    def get_personal_url(self):
        return self.slug or slugify(self.name)

    def save(self, *args, **kwargs):
        if self.date > timezone.now().date():
            raise ValidationError("The date cannot be in the future!")
        super(Artwork, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if os.path.isfile(self.image.path):
            os.remove(self.image.path)

        super(Artwork, self).delete(*args, **kwargs)

    def __str__(self):
        return f"{self.author.name} | {self.title}"

    class Meta:
        verbose_name = _("Artwork")
        verbose_name_plural = _("Artworks")


class Event(models.Model):

    event_name = models.CharField(
        _("Title"), max_length=255, help_text="Name of event.", unique=True
    )
    event_description = models.TextField(_("Content"), help_text="Description")
    date = models.DateField(_("Date"), help_text="Date of event")
    image = models.ImageField(
        _("Event preview"), help_text=_("Preview image for event"), upload_to=wrapper
    )

    location = models.ForeignKey(
        Gallery,
        verbose_name=_("Location"),
        on_delete=models.PROTECT,
        help_text=_("Location of event."),
    )

    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name=_("Author account")
    )
    slug = models.SlugField(_("Slug"), unique=True, editable=False, null=True)

    class Meta:
        ordering = ["-date"]
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.event_name)
        super(Event, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if os.path.isfile(self.image.path):
            os.remove(self.image.path)

        super(Event, self).delete(*args, **kwargs)

    def __str__(self):
        return self.event_name
