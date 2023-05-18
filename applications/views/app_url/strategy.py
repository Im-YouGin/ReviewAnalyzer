from abc import ABC, abstractmethod

from applications.models import Application
from common.constants import AppMarket
from scraping.app_store.app_details import AppStoreAppDetailsScraper
from scraping.google_play.app_details import GooglePlayAppDetailsScraper
from scraping.google_search.functions import search_app


class BaseAppUrlStrategy(ABC):
    market: AppMarket
    other_market: AppMarket

    def __init__(self, app_identifiers):
        self.app_identifiers = app_identifiers

    @property
    def app_id(self):
        return self.app_identifiers["app_id"]

    @abstractmethod
    def get_app_details(self):
        raise NotImplementedError

    @abstractmethod
    def get_app_market_specific_attrs(self):
        raise NotImplementedError

    def process(self):
        app_obj = self.get_existing_app()
        created = False

        if not app_obj:
            app_details = self.get_app_details()

            app_identifiers_other_market = self.get_app_identifiers_other_market(
                name=app_details["name"], developer=app_details["developer"]
            )
            if app_identifiers_other_market:
                app_obj = self.get_existing_app_other_market(
                    app_id=app_identifiers_other_market["app_id"]
                )
                if app_obj:
                    setattr(app_obj, f"{self.market}_id", self.app_id)
                    app_obj.__dict__.update(self.get_app_market_specific_attrs())
                    app_obj.save()

            if not app_obj:
                values_dict = {
                    "name": app_details["name"],
                    **{
                        f"{self.market}_id": self.app_id,
                        **self.get_app_market_specific_attrs(),
                    },
                    **{
                        attr.replace("app", self.other_market): value
                        for attr, value in app_identifiers_other_market.items()
                    },
                }
                app_obj = Application(**values_dict)
                app_obj.save()

                created = True

        return app_obj, created

    def get_existing_app(self):
        return self.__get_application_by_market_and_id(
            app_id=self.app_id, market=self.market
        )

    def get_existing_app_other_market(self, app_id):
        return self.__get_application_by_market_and_id(
            app_id=app_id, market=self.other_market
        )

    def get_app_identifiers_other_market(self, name, developer):
        return search_app(name, developer, market=self.other_market)

    @staticmethod
    def __get_application_by_market_and_id(app_id, market):
        return Application.objects.filter(**{f"{market}_id": app_id}).first()


class AppStoreAppUrlStrategy(BaseAppUrlStrategy):
    market = AppMarket.APP_STORE
    other_market = AppMarket.GOOGLE_PLAY

    @property
    def app_slug(self):
        return self.app_identifiers["app_slug"]

    def get_app_details(self):
        scraper = AppStoreAppDetailsScraper(app_id=self.app_id, app_slug=self.app_slug)
        return scraper.get_details()

    def get_app_market_specific_attrs(self):
        return {"app_store_slug": self.app_slug}


class GooglePlayAppUrlStrategy(BaseAppUrlStrategy):
    market = AppMarket.GOOGLE_PLAY
    other_market = AppMarket.APP_STORE

    def get_app_details(self):
        scraper = GooglePlayAppDetailsScraper(app_id=self.app_id)
        return scraper.get_details()

    def get_app_market_specific_attrs(self):
        pass
