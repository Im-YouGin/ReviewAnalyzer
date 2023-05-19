from abc import ABC, abstractmethod

from django.db import transaction
from django.utils import timezone

from applications.models import Application, Review
from common.constants import BATCH_SIZE, AppMarket, AppStatus


class BaseReviewScrapingProcessRunner(ABC):
    _process_name: str
    _market: AppMarket

    def __init__(self, application_id):
        self.application = Application.objects.filter(id=application_id).first()

    @abstractmethod
    def _get_scraper(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def _logger(self):
        raise NotImplementedError

    def scrape(self):
        self._logger.info(
            f"Starting scraping {self.application.name} reviews from {self._market.pretty}."
        )

        if not self._continue_processing():
            self._logger.info(
                f"Exiting... {self.application.name} reviews are already being updated."
            )
            return

        self._set_status(AppStatus.UPDATING)

        try:
            scraper = self._get_scraper()
            for page in scraper.get_reviews():
                to_create = [
                    Review(
                        application=self.application,
                        content=r["content"],
                        username=r["username"],
                        stars=r["stars"],
                        market=self._market,
                        source_id=r["id"],
                        source_created_at=r["created_at"],
                    )
                    for r in page
                ]

                if to_create:
                    self._logger.info(
                        f"Creating {len(to_create)} new {self._market.pretty} reviews for {self.application.name}."
                    )

                with transaction.atomic():
                    Review.objects.bulk_create(
                        objs=to_create, batch_size=BATCH_SIZE, ignore_conflicts=True
                    )

        except Exception as e:
            self._logger.exception(
                f"Something went wrong trying to scrape review for {self.application.name}.\n{e}"
            )

        finally:
            self._set_status(AppStatus.READY)

        setattr(self.application, f"{self._market}_last_scraped_at", timezone.now())

        self._logger.info(
            f"Finished scraping {self._market.pretty} review on {self.application.name}."
        )

    def _continue_processing(self):
        return self.application or self._get_status() is AppStatus.UPDATING

    def _get_status(self):
        return getattr(self.application, f"{self._market}_status")

    def _set_status(self, status):
        setattr(self.application, f"{self._market}_status", status)
        self.application.save()
