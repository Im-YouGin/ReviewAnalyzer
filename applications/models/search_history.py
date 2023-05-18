from django.conf import settings
from django.db import models

from common.models import TimestampedModel, UUIDModel


class SearchHistory(UUIDModel, TimestampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    application = models.ForeignKey(
        "applications.Application", on_delete=models.CASCADE
    )
