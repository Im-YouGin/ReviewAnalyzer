import json
import logging
from datetime import datetime
from typing import Optional, Union

import pytz

from applications.models import Application
from scraping.common.app_reviews.scraper import BaseAppReviewsScraper
from scraping.google_play.constants import (
    GOOGLE_PLAY_APP_REVIEWS_URL,
    NULL,
    GooglePlayOrdering,
)
from scraping.google_play.constants.regex import GOOGLE_PLAY_REVIEWS_REGEX

logger = logging.getLogger("review_analyzer")


class GooglePlayAppReviewsScraper(BaseAppReviewsScraper):
    def __init__(
        self, application: Application, min_created_at: Optional[datetime] = None
    ):
        super().__init__()

        self.application = application
        self.app_id = application.google_play_id

        self._min_created_at = min_created_at or pytz.utc.localize(datetime.min)

        self.__pagination_token = None

    def get_reviews(self):
        min_date_reached = False

        while True:
            if min_date_reached:
                break

            try:
                review_objects, self.__pagination_token = self._send_request()
            except (TypeError, IndexError):
                break

            review_objects_filtered = []
            for obj in review_objects:
                review_dict = self._parse_review_object(obj)

                if review_dict["created_at"] <= self._min_created_at:
                    min_date_reached = True
                    break

                review_objects_filtered.append(review_dict)

            yield review_objects_filtered

            if isinstance(self.__pagination_token, list):
                break

            self._perform_anti_blocking_actions()

    def _send_request(self):
        response = self._session.post(
            GOOGLE_PLAY_APP_REVIEWS_URL,
            data=self.__build_request_payload(),
        )

        matched_data = json.loads(GOOGLE_PLAY_REVIEWS_REGEX.findall(response.text)[0])

        return json.loads(matched_data[0][2])[0], json.loads(matched_data[0][2])[-1][-1]

    def _create_session(self):
        session = super()._create_session()
        session.headers.update({"content-type": "application/x-www-form-urlencoded"})

        return session

    def __build_request_payload(
        self,
        ordering: GooglePlayOrdering = GooglePlayOrdering.MOST_RECENT,
        count: int = 1000,
        stars: Union[int, str] = NULL,
    ):
        return (
            f"f.req=%5B%5B%5B%22UsvDTd%22%2C%22%5Bnull%2Cnull%2C%5B2%2C{ordering}%2C%5B{count}%2Cnull%2C"
            + (
                f"%5C%22{self.__pagination_token}%5C%22"
                if self.__pagination_token
                else "null"
            )
            + f"%5D%2Cnull%2C%5Bnull%2C{stars}%5D%5D%2C%5B%5C%22{self.app_id}%5C%22%2C7%5D%5D%22%2Cnull%2C%22generic%22%5D%5D%5D"
        ).encode()

    @staticmethod
    def _parse_review_object(review_object):
        return {
            "id": review_object[0],
            "username": review_object[1][0],
            "content": review_object[4],
            "stars": review_object[2],
            "created_at": pytz.utc.localize(
                datetime.fromtimestamp(review_object[5][0])
            ),
        }
