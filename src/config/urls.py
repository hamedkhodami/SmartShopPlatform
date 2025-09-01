from typing import Any

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import URLPattern, URLResolver, include
from django.urls import path as dj_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# ----------------------------------------------------------------


# ---Swagger------------------------------------------------------
schema_view = get_schema_view(
    openapi.Info(
        title="Swagger API",
        default_version="v1",
        description="Swagger API",
        license=openapi.License(name="MIT Lisense"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
# ----------------------------------------------------------------


# ---API----------------------------------------------------------
def path(url: str, *args: Any, **kwargs: Any) -> URLPattern:
    url = f"{settings.API_URL_LABEL}/{settings.API_VERSION}/{url}"
    return dj_path(url, *args, **kwargs)


# ----------------------------------------------------------------


# ---URLPATTERNS--------------------------------------------------
urlpatterns_swagger = [
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

urlpatterns_api: list[URLPattern | URLResolver] = []

urlpatterns_tools = [
    dj_path("rosetta/", include("rosetta.urls")),
    path("admin/", admin.site.urls),
]

urlpatterns = [
    *urlpatterns_swagger,
    *urlpatterns_api,
    *urlpatterns_tools,
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# ----------------------------------------------------------------
