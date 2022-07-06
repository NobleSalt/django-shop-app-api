from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from core.views import index

handler404 = 'core.views.error_404_view'
urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("api/", include("api.urls")),
        path("", index),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

# [
#     # static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
# ]
