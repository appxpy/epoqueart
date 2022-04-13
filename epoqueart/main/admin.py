from django.contrib import admin
from .models import Country, City, Currency, Gallery, Author, Artwork_Type, Artwork_Status, Artwork, Event

[admin.site.register(i) for i in [Country, City, Currency, Gallery, Author, Artwork_Type, Artwork_Status, Artwork, Event]]
