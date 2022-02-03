from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

from main import views

handler404 = "main.views.handler404"
handler500 = "main.views.handler500"
handler403 = "main.views.handler403"
handler401 = "main.views.handler401"
handler400 = "main.views.handler400"

urlpatterns = [
    path("", views.home, name="home"),
    path("gallery/", views.gallery, name="gallery"),
    path("api/gallery/search", views.gallery_search_api, name="gallery_search_api"),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("logout/", views.logout_view, name="user_logout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
