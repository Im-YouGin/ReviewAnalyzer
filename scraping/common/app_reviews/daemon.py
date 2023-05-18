import concurrent.futures
import logging
from abc import ABC, abstractmethod
from typing import Type, Union

from applications.models import Application
from common.constants import AppMarket, AppStatus
from scraping.app_store.app_reviews.runner import AppStoreReviewScrapingProcessRunner
from scraping.google_play.app_reviews.runner import (
    GooglePlayReviewScrapingProcessRunner,
)

logger = logging.getLogger(__name__)


class BaseAllReviewScrapingDaemon(ABC):
    max_session_app_count: int
    market: AppMarket
    scraping_runner_class: Union[
        Type[AppStoreReviewScrapingProcessRunner],
        Type[GooglePlayReviewScrapingProcessRunner],
    ]

    def run(self):
        logger.info(f"Starting {self.market.pretty} reviews scraping daemon.")

        application_ids_to_scrape = self._get_application_ids_to_scrape()

        logger.info(
            f"{self.market.pretty} review scraping daemon found {len(application_ids_to_scrape)} to update."
        )

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            executor.map(
                lambda _id: self.scraping_runner_class(_id).scrape(),
                application_ids_to_scrape,
            )

        logger.info(f"{self.market.pretty} reviews scraping daemon finished.")

    def _get_application_ids_to_scrape(self):
        return (
            Application.objects.exclude(**{f"{self.market}_status": AppStatus.UPDATING})
            .order_by(f"{self.market}_last_scraped_at")
            .values_list("id", flat=True)[: self.max_session_app_count]
        )
