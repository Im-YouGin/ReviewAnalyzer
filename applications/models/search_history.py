from django.conf import settings
from django.db import models

from common.models import TimestampedModel, UUIDModel


class SearchHistory(UUIDModel, TimestampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    application = models.ForeignKey(
        "applications.Application", on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "application", "created_at"],
                name="uc_search_history_user_app_created_at",
            ),
        ]
