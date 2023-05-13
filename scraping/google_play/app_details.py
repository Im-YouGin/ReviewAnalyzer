import datetime
import json
import logging
import random
import re
import time
from typing import Optional, Union

import pytz
import requests
from django.utils import timezone

from scraping.common.app_review import BaseAppReviewScraper
from scraping.google_play.constants import (
    GOOGLE_PLAY_APP_REVIEWS_URL,
    NULL,
    GooglePlayOrdering,
)

GOOGLE_PLAY_REVIEWS_REGEX = re.compile("\)]}'\n\n([\s\S]+)")

logger = logging.getLogger(__file__)


class GooglePlayAppReviewScraper(BaseAppReviewScraper):
    def __init__(
        self, package_name: str, min_created_at: Optional[datetime.datetime] = None
    ):
        self.package_name = package_name

        self.__min_created_at = min_created_at or timezone.now() - datetime.timedelta(
            weeks=2
        )
        self.__reviews = []
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

            for obj in review_objects:
                review_dict = self.__parse_review_object(obj)

                if review_dict["created_at"] <= self.__min_created_at:
                    min_date_reached = True
                    break

                yield review_dict

            if isinstance(self.__pagination_token, list):
                break

            if not min_date_reached:
                time.sleep(random.choice([1, 2, 3]))

    def _send_request(self):
        response = requests.post(
            GOOGLE_PLAY_APP_REVIEWS_URL,
            data=self.__build_request_payload(),
            headers={"content-type": "application/x-www-form-urlencoded"},
        )

        matched_data = json.loads(GOOGLE_PLAY_REVIEWS_REGEX.findall(response.text)[0])

        return json.loads(matched_data[0][2])[0], json.loads(matched_data[0][2])[-1][-1]

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
            + f"%5D%2Cnull%2C%5Bnull%2C{stars}%5D%5D%2C%5B%5C%22{self.package_name}%5C%22%2C7%5D%5D%22%2Cnull%2C%22generic%22%5D%5D%5D"
        ).encode()

    @staticmethod
    def __parse_review_object(review_object):
        return {
            "username": review_object[1][0],
            "content": review_object[4],
            "stars": review_object[2],
            "app_version": review_object[10],
            "created_at": pytz.utc.localize(
                datetime.datetime.fromtimestamp(review_object[5][0])
            ),
        }
