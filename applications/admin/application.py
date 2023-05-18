from django.contrib import admin

from applications.models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    fields = (
        "id",
        "name",
        "app_store_id",
        "app_store_slug",
        "google_play_id",
        "created_at",
        "modified_at",
    )
    readonly_fields = ("id", "created_at", "modified_at")
    list_display = ("id", "name", "app_store_id", "google_play_id")
    search_fields = (
        "name",
        "app_store_id",
        "app_store_slug",
        "google_play_id",
    )
    ordering = ["-modified_at"]
