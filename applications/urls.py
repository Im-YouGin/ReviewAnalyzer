from django.urls import path

from . import views

app_name = "applications"


urlpatterns = [
    path("app-url/", views.AppUrlView.as_view(), name="app-url"),
    path("<uuid:pk>/", views.ApplicationView.as_view(), name="application"),
    path(
        "<uuid:pk>/analytics/",
        views.ApplicationAnalyticsView.as_view(),
        name="application-analytics",
    ),
    path(
        "recent-searches/", views.RecentSearchesView.as_view(), name="recent-searches"
    ),
]
