from django.contrib import admin

from applications.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    fields = (
        "id",
        "application",
        "content",
        "username",
        "stars",
        "market",
        "sentiment_str",
        "sentiment_score",
        "source_id",
        "source_created_at",
    )
    readonly_fields = ("id", "created_at", "modified_at")
    list_display = (
        "id",
        "application",
        "username",
        "market",
        "stars",
        "sentiment_str",
        "content",
    )
    list_filter = ("sentiment_str",)
