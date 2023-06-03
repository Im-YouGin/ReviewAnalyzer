from django.db import models, transaction

from common.constants import AppStatus
from common.models import TimestampedModel, UUIDModel
from scraping.tasks import (
    q_scrape_app_store_app_reviews,
    q_scrape_google_play_app_reviews,
)


class Application(UUIDModel, TimestampedModel):
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    # AppStore - START
    app_store_id = models.CharField(max_length=16, blank=True)
    app_store_slug = models.CharField(max_length=127, blank=True)
    app_store_status = models.CharField(
        choices=AppStatus.choices(), max_length=32, default=AppStatus.READY
    )
    app_store_last_scraped_at = models.DateTimeField(null=True, blank=True)
    # AppStore - END

    # GooglePlay - START
    google_play_id = models.CharField(max_length=127, blank=True)
    google_play_status = models.CharField(
        choices=AppStatus.choices(), max_length=32, default=AppStatus.READY
    )
    google_play_last_scraped_at = models.DateTimeField(null=True, blank=True)
    # GooglePlay - END

    @property
    def status(self):
        return (
            AppStatus.UPDATING
            if self.app_store_status == AppStatus.UPDATING
            or self.google_play_status == AppStatus.UPDATING
            else AppStatus.READY
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["app_store_id"],
                name="unique_app_store_id_non_blank",
                condition=~models.Q(app_store_id=""),
            ),
            models.UniqueConstraint(
                fields=["app_store_slug"],
                name="unique_app_store_slug_non_blank",
                condition=~models.Q(app_store_slug=""),
            ),
            models.UniqueConstraint(
                fields=["google_play_id"],
                name="unique_google_play_id_non_blank",
                condition=~models.Q(google_play_id=""),
            ),
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__cache_previous_values()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        created = self.created_at is None

        super().save(*args, **kwargs)

        self.__post_save(created)

    def __post_save(self, created):
        def enqueue_scraping_tasks():
            if (
                created
                or self.__previous_app_store_id is None
                and self.app_store_id is not None
            ):
                q_scrape_app_store_app_reviews.delay(self.id)

            if (
                created
                or self.__previous_google_play_id is None
                and self.google_play_id is not None
            ):
                q_scrape_google_play_app_reviews.delay(self.id)

        transaction.on_commit(enqueue_scraping_tasks)

        self.__cache_previous_values()

    def __cache_previous_values(self):
        self.__previous_app_store_id = self.app_store_id
        self.__previous_google_play_id = self.google_play_id
