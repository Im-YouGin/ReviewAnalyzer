import logging

from common.constants import AppMarket
from scraping.app_store.app_reviews.scraper import AppStoreAppReviewsScraper
from scraping.common.app_reviews.runner import BaseReviewScrapingProcessRunner

logger = logging.getLogger(__name__)


class AppStoreReviewScrapingProcessRunner(BaseReviewScrapingProcessRunner):
    _process_name = "app-store-review-scraping"
    _market = AppMarket.APP_STORE

    def _get_scraper(self):
        return AppStoreAppReviewsScraper(self.application)

    @property
    def _logger(self):
        return logger
