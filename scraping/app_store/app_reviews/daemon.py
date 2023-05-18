import logging

from applications.models import Application
from common.constants import AppMarket, AppStatus
from scraping.app_store.app_reviews.runner import AppStoreReviewScrapingProcessRunner
from scraping.common.app_reviews.daemon import BaseAllReviewScrapingDaemon

logger = logging.getLogger(__name__)


class AppStoreAllReviewScrapingDaemon(BaseAllReviewScrapingDaemon):
    max_session_app_count = 50
    market = AppMarket.APP_STORE
    scraping_runner_class = AppStoreReviewScrapingProcessRunner
