import logging

from django.db.models import Max

from common.constants import AppMarket
from scraping.common.app_reviews.runner import BaseReviewScrapingProcessRunner
from scraping.google_play.app_reviews.scraper import GooglePlayAppReviewsScraper

logger = logging.getLogger(__name__)


class GooglePlayReviewScrapingProcessRunner(BaseReviewScrapingProcessRunner):
    _market = AppMarket.GOOGLE_PLAY

    def _get_scraper(self):
        most_recent_review_time = self.application.review_set.filter(
            market=self._market
        ).aggregate(Max("source_created_at"))["source_created_at__max"]
        return GooglePlayAppReviewsScraper(
            self.application, min_created_at=most_recent_review_time
        )

    @property
    def _logger(self):
        return logger
