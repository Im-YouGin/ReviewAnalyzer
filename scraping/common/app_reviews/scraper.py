import random
import time
from abc import ABC, abstractmethod

from scraping.common.mixins import RequestsMixin


class BaseAppReviewsScraper(ABC, RequestsMixin):
    def __init__(self, *args, **kwargs):
        self._session = self._create_session()

    @abstractmethod
    def get_reviews(self):
        raise NotImplementedError

    @abstractmethod
    def _parse_review_object(self, *args, **kwargs):
        raise NotImplementedError

    def _perform_anti_blocking_actions(self):
        self.__rotate_session_user_agent()
        time.sleep(random.random() * 2)  # nosec

    def __rotate_session_user_agent(self):
        self._session.headers.update({"User-Agent": self._ua.random})
