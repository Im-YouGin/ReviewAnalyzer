import logging

from common.constants import AppMarket
from scraping.app_store.app_reviews.runner import AppStoreReviewScrapingProcessRunner
from scraping.common.app_reviews.daemon import BaseAllReviewScrapingDaemon

logger = logging.getLogger("review_analyzer")


class AppStoreAllReviewScrapingDaemon(BaseAllReviewScrapingDaemon):
    max_session_app_count = 50
    market = AppMarket.APP_STORE
    scraping_runner_class = AppStoreReviewScrapingProcessRunner
