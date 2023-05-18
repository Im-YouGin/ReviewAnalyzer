import re
from datetime import datetime
from urllib.parse import parse_qs, urlparse

import pytz

from common.constants import GET, AppMarket
from scraping.app_store.constants import (
    APP_STORE_APP_HOME_URL,
    APP_STORE_APP_REVIEWS_URL,
    APP_STORE_BASE_URL,
)
from scraping.common.app_reviews.scraper import BaseAppReviewsScraper

APP_STORE_ACCESS_TOKEN_REGEX = re.compile(
    r"(?<=token%22%3A%22)[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+"
)


class AppStoreAppReviewsScraper(BaseAppReviewsScraper):
    SESSION_REVIEW_COUNT_LIMIT = 5000

    def __init__(self, application):
        super().__init__()

        self.application = application
        self.app_id = application.app_store_id
        self.app_slug = application.app_store_slug

        self.__app_home_url = self.__build_app_home_url()
        self.__app_reviews_url = self.__build_app_reviews_url()

    def get_reviews(self):
        self._set_reviews_endpoint_headers_and_params()

        fetched_review_counter = 0

        while True:
            response = self._request(self.__app_reviews_url, method=GET).json()

            review_container = response["data"]
            review_dicts = [self._parse_review_object(obj) for obj in review_container]
            review_dicts_non_existing = self._filter_non_existing_reviews(review_dicts)

            yield review_dicts_non_existing

            fetched_review_counter += len(review_dicts_non_existing)
            if fetched_review_counter >= self.SESSION_REVIEW_COUNT_LIMIT:
                break

            next_offset = self._get_next_offset(response)
            is_offset_changed = self._update_offset_param(next_offset)
            if not is_offset_changed:
                # If offset is not changed, it means that we fetched all reviews
                break

            self._perform_anti_blocking_actions()

    def _set_reviews_endpoint_headers_and_params(self):
        response = self._request(self.__app_home_url, method=GET)
        access_token = APP_STORE_ACCESS_TOKEN_REGEX.findall(response.text)[0]

        self._session.headers.update(
            {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": APP_STORE_BASE_URL,
                "Referer": APP_STORE_BASE_URL,
            }
        )

        self._session.params = {
            "platform": "web",
            "limit": 20,  # AppStore API allows to fetch at most 20 reviews at once
            "offset": 0,
        }

    def _parse_review_object(self, review_object):
        review_attrs = review_object["attributes"]

        return {
            "id": review_object["id"],
            "username": review_attrs["userName"],
            "content": review_attrs["review"],
            "stars": review_attrs["rating"],
            "created_at": pytz.utc.localize(
                datetime.strptime(review_attrs["date"], "%Y-%m-%dT%H:%M:%SZ")
            ),
        }

    def _filter_non_existing_reviews(self, reviews):
        existing_source_ids = self.application.review_set.filter(
            market=AppMarket.APP_STORE, source_id__in={r["id"] for r in reviews}
        ).values_list("source_id", flat=True)

        return [r for r in reviews if r["id"] not in existing_source_ids]

    @staticmethod
    def _get_next_offset(response):
        if next_url := response.get("next"):
            query_params = parse_qs(urlparse(next_url).query)
            if offset := query_params.get("offset"):
                return int(offset[0])

    def _update_offset_param(self, next_offset):
        if next_offset and next_offset > self._session.params["offset"]:
            self._session.params["offset"] = next_offset
            return True
        return False

    def __build_app_home_url(self):
        return APP_STORE_APP_HOME_URL.format(app_slug=self.app_slug, app_id=self.app_id)

    def __build_app_reviews_url(self):
        return APP_STORE_APP_REVIEWS_URL.format(app_id=self.app_id)
