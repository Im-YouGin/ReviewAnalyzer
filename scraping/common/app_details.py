from abc import ABC, abstractmethod

from scraping.common.mixins import RequestsMixin


class BaseAppDetailsScraper(ABC, RequestsMixin):
    def __init__(self, *args, **kwargs):
        self._session = self._create_session()

    @abstractmethod
    def get_details(self):
        raise NotImplementedError

    def _parse_details(self, *args, **kwargs):
        raise NotImplementedError
