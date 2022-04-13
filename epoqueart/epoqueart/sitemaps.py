from django.contrib import sitemaps
from django.urls import reverse


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "daily"

    def items(self):
        return [
            "home",
            "about",
            "artists",
            "collection",
            "interior",
            "on_demand",
            "gallery",
        ]

    def location(self, item):
        return reverse(item)
