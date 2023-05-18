from django.db import models
from django.db.models import UniqueConstraint

from analytics.constants.enums import Sentiment
from common.constants import AppMarket, Star
from common.models import TimestampedModel, UUIDModel


class Review(UUIDModel, TimestampedModel):
    application = models.ForeignKey(
        "applications.Application", on_delete=models.CASCADE
    )

    content = models.TextField()
    username = models.CharField(max_length=255)
    stars = models.IntegerField(choices=Star.choices())
    market = models.CharField(choices=AppMarket.choices())
    source_id = models.CharField(max_length=255)
    source_created_at = models.DateTimeField()

    # Sentiment data - START
    sentiment_str = models.CharField(
        max_length=20, choices=Sentiment.choices(), blank=True
    )
    sentiment_score = models.FloatField(null=True, blank=True)
    is_sentiment_analyzed = models.BooleanField(default=False)
    # Sentiment data - END

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["market", "source_id"], name="uc_review_source_source_id"
            ),
        ]

        indexes = [
            models.Index(fields=["source_id"], name="review_source_id_index"),
        ]

    def __str__(self):
        return f"{self.username}|{self.application}|{self.stars}"
