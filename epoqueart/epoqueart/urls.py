from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from django.conf.urls.static import static
from .sitemaps import StaticViewSitemap

from main import views

handler400 = "main.views.handler400"
handler401 = "main.views.handler401"
handler403 = "main.views.handler403"
handler404 = "main.views.handler404"
handler500 = "main.views.handler500"

sitemaps = {
    'sitemaps': StaticViewSitemap
}

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("artists/", views.artists, name="artists"),
    path("artist/<slug:slug>/", views.artist, name="artist"),
    path("collection", views.collection, name="collection"),
    path("interiors/", views.interior, name="interior"),
    path("on demand/", views.on_demand, name="on_demand"),
    path("gallery/", views.gallery, name="gallery"),
    path("api/gallery/search", views.gallery_search_api, name="gallery_search_api"),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path("logout/", views.logout_view, name="user_logout"),
    # Error handlers
    path('400/', views.handler400),
    path('401/', views.handler401),
    path('403/', views.handler403),
    path('404/', views.handler404),
    path('500/', views.handler500),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
