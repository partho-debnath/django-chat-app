from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api-doc/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("chat/", include("chat.urls", namespace="chat")),
    path("user/", include("user.urls", namespace="user")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
