from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string

from common.models import TimestampedModel, UUIDModel


class EmailConfirmationToken(UUIDModel, TimestampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(
        max_length=50,
        unique=True,
    )
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = get_random_string(length=50)

        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=5)

        super().save(*args, **kwargs)
