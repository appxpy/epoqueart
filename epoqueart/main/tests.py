import re
import shutil
from django.conf import settings
from django.test import TestCase

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.utils import timezone
from django.contrib import auth
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage

import os

from .models import (
    CustomUser,
    Author,
    Artwork_Type,
    Artwork_Status,
    Artwork,
    Country,
    City,
    Currency,
    Gallery,
)

BLACK_PIXEL_IMAGE = b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"


class BasicTest(TestCase):
    def setUp(self):
        test_user = CustomUser.objects.create_user(
            email="testuser@epoque.art", password="12345", is_superuser=True
        )
        test_user.save()

    def test_login_logout(self):
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)
        self.client.login(username="testuser@epoque.art", password="12345")
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        resp = self.client.get(reverse("user_logout"))
        self.assertEqual(resp.status_code, 302)
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_robots_pages(self):
        try:
            abs_path = finders.find("robots.txt")
            self.assertTrue(staticfiles_storage.exists(abs_path))
        except Exception:
            raise AssertionError("robots.txt doesn't exist.")
        resp = self.client.get("/sitemap.xml")
        self.assertEqual(resp.status_code, 200)

    def test_static_files(self):
        try:
            absolute_path = finders.find("favicon.svg")
            self.assertTrue(staticfiles_storage.exists(absolute_path))
        except Exception:
            raise AssertionError("favicon.svg doesn't exist.")

    def test_404_page(self):
        resp = self.client.get("unknown-page")
        self.assertEqual(404, resp.status_code)
        self.assertTemplateUsed(resp, "main/errors/404.html")


class AdvancedTest(TestCase):
    def tearDown(self):
        shutil.rmtree(settings.MEDIA_ROOT)
        if os.path.exists(settings.MEDIA_ROOT + "_backup"):
            os.rename(settings.MEDIA_ROOT + "_backup", settings.MEDIA_ROOT)

    def setUp(self):
        if not os.path.exists(settings.MEDIA_ROOT + "_backup"):
            shutil.copytree(settings.MEDIA_ROOT, settings.MEDIA_ROOT + "_backup")
        self.test_user = CustomUser.objects.create_user(
            email="testuser@epoque.art", password="12345", is_superuser=True
        )

        self.author1 = Author.objects.create(
            preview_image=SimpleUploadedFile(
                name="test_image.jpg",
                content=BLACK_PIXEL_IMAGE,
                content_type="image/jpeg",
            ),
            image=SimpleUploadedFile(
                name="test_image.jpg",
                content=BLACK_PIXEL_IMAGE,
                content_type="image/jpeg",
            ),
            name="Test Author 01",
            qualification="Test Qualification 01",
            description="Test Description 01",
        )

        self.author2 = Author.objects.create(
            preview_image=SimpleUploadedFile(
                name="test_image.jpg",
                content=BLACK_PIXEL_IMAGE,
                content_type="image/jpeg",
            ),
            image=SimpleUploadedFile(
                name="test_image.jpg",
                content=BLACK_PIXEL_IMAGE,
                content_type="image/jpeg",
            ),
            name="Test Author 02",
            qualification="Test Qualification 02",
            description="Test Description 02",
        )

        self.artwork_type = Artwork_Type.objects.create(artwork_type_name="Painting")

        self.artwork_status_available = Artwork_Status.objects.create(
            artwork_status_name="Available", artwork_is_available=True
        )

        self.artwork_status_reserved = Artwork_Status.objects.create(
            artwork_status_name="Reserved", artwork_is_available=False
        )

        self.artwork_status_sold = Artwork_Status.objects.create(
            artwork_status_name="Sold", artwork_is_available=False
        )

        self.country = Country.objects.create(country="USA")

        self.city = City.objects.create(
            city_name="Miami", postal_code="33101", country=self.country
        )

        self.currency = Currency.objects.create(
            country=self.country,
            currency_name="US Dollar",
            currency_short="USD",
            currency_symbol="$",
        )

        self.gallery = Gallery.objects.create(
            gallery_name="EpoqueArt - Miami",
            gallery_address="108 NE 2nd St, Boca Raton, FL 33432, USA",
            gallery_description="Sample description",
            city=self.city,
        )

        self.artwork_01 = Artwork.objects.create(
            title="Artwork 1",
            author=self.author1,
            date=timezone.now().date(),
            image=SimpleUploadedFile(
                name="test_image.jpg",
                content=BLACK_PIXEL_IMAGE,
                content_type="image/jpeg",
            ),
            type=self.artwork_type,
            width=50,
            height=50,
            measure="Inch",
            materials="Paint, Paper",
            price=1000,
            currency=self.currency,
            is_nft_linked=True,
            location=self.gallery,
            status=self.artwork_status_available,
        )

        self.artwork_02 = Artwork.objects.create(
            title="Artwork 2",
            author=self.author2,
            date=timezone.now().date() - timezone.timedelta(days=5),
            image=SimpleUploadedFile(
                name="test_image.jpg",
                content=BLACK_PIXEL_IMAGE,
                content_type="image/jpeg",
            ),
            type=self.artwork_type,
            width=300,
            height=400,
            measure="Centimeters",
            materials="Paint, Paper",
            price=3000,
            currency=self.currency,
            is_nft_linked=False,
            location=self.gallery,
            status=self.artwork_status_available,
        )

        self.artwork_03 = Artwork.objects.create(
            title="Artwork 3",
            author=self.author1,
            date=timezone.now().date() - timezone.timedelta(days=5),
            image=SimpleUploadedFile(
                name="test_image.jpg",
                content=BLACK_PIXEL_IMAGE,
                content_type="image/jpeg",
            ),
            type=self.artwork_type,
            width=300,
            height=400,
            measure="Centimeters",
            materials="Paint, Paper",
            price=3000,
            currency=self.currency,
            is_nft_linked=False,
            location=self.gallery,
            status=self.artwork_status_sold,
        )

        self.artwork_04 = Artwork.objects.create(
            title="Artwork 3",
            author=self.author2,
            date=timezone.now().date() - timezone.timedelta(days=360),
            image=SimpleUploadedFile(
                name="test_image.jpg",
                content=BLACK_PIXEL_IMAGE,
                content_type="image/jpeg",
            ),
            type=self.artwork_type,
            width=200,
            height=600,
            measure="Centimeterss",
            materials="Paint, Paper",
            price=2000,
            currency=self.currency,
            is_nft_linked=True,
            location=self.gallery,
            status=self.artwork_status_reserved,
        )

    def test_netgallery_reach_admin(self):
        self.client.login(email="testuser@epoque.art", password="12345")
        resp = self.client.get(reverse("gallery"))
        self.assertEqual(resp.status_code, 200)

    def test_netgallery_reach(self):
        resp = self.client.get(reverse("gallery"))
        self.assertEqual(resp.status_code, 200)

    def test_netgallery_template(self):
        resp = self.client.get(reverse("gallery"))
        self.assertTemplateUsed(resp, "main/gallery.html")

    def test_netgallery_context(self):
        resp = self.client.get(reverse("gallery"))
        self.assertEqual(int(resp.context["price__max"]), 3000)
        self.assertEqual(int(resp.context["price__min"]), 1000)

        self.assertEqual(int(resp.context["year__max"]), 2022)
        self.assertEqual(int(resp.context["year__min"]), 2021)

        self.assertEqual(int(resp.context["nft"]), False)

        self.assertEqual(len(resp.context["artworks"]), 2)

    def test_artwork_converting(self):
        self.assertEqual(
            Artwork.objects.filter(measure="Centimeters").first().get_size_inch(),
            (118, 157),
        )
        self.assertEqual(
            Artwork.objects.filter(measure="Inch").first().get_size_cm(), (127, 127)
        )

    def test_home_page(self):
        resp = self.client.get(reverse("home"))
        self.assertTemplateUsed(resp, "main/pages/home.html")
        self.assertEqual(resp.status_code, 200)

    def test_about_page(self):
        resp = self.client.get(reverse("about"))
        self.assertTemplateUsed(resp, "main/pages/about.html")
        self.assertEqual(resp.status_code, 200)

    def test_artists_page(self):
        resp = self.client.get(reverse("artists"))
        self.assertTemplateUsed(resp, "main/pages/artists.html")
        self.assertEqual(resp.status_code, 200)

    def test_on_demand_page(self):
        resp = self.client.get(reverse("on_demand"))
        self.assertTemplateUsed(resp, "main/pages/on-demand.html")
        self.assertEqual(resp.status_code, 200)
