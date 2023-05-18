from common.constants import AppMarket
from scraping.common.app_reviews.daemon import BaseAllReviewScrapingDaemon
from scraping.google_play.app_reviews.runner import (
    GooglePlayReviewScrapingProcessRunner,
)


class GooglePlayAllReviewScrapingDaemon(BaseAllReviewScrapingDaemon):
    max_session_app_count = 100
    market = AppMarket.GOOGLE_PLAY
    scraping_runner_class = GooglePlayReviewScrapingProcessRunner
