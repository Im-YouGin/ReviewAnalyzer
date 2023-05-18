from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/",
        include(
            [
                path("applications/", include("applications.urls")),
                path("authentication/", include("authentication.urls")),
            ]
        ),
    ),
]
