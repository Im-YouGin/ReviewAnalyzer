import json

from scraping.common.app_details import BaseAppDetailsScraper
from scraping.google_play.constants import GOOGLE_PLAY_APP_HOME_URL
from scraping.google_play.constants.regex import (
    GOOGLE_PLAY_DATA_KEY_REGEX,
    GOOGLE_PLAY_DATA_VALUE_REGEX,
    GOOGLE_PLAY_SCRIPT_REGEX,
)


class GooglePlayAppDetailsScraper(BaseAppDetailsScraper):
    def __init__(self, app_id: str):
        super().__init__()

        self.app_id = app_id

        self.__app_home_url = self.__build_app_home_url()

    def get_details(self):
        response = self._session.get(self.__app_home_url)

        dataset = self._get_dataset_from_scripts(response)
        details = self._parse_details(dataset)

        return details

    @staticmethod
    def _get_dataset_from_scripts(response):
        return {
            k_match[0]: json.loads(v_match[0])
            for script_match in GOOGLE_PLAY_SCRIPT_REGEX.findall(response.text)
            if (
                (k_match := GOOGLE_PLAY_DATA_KEY_REGEX.findall(script_match))
                and (v_match := GOOGLE_PLAY_DATA_VALUE_REGEX.findall(script_match))
            )
        }

    def _parse_details(self, dataset):
        ds5 = dataset["ds:5"]

        return {
            "name": ds5[1][2][0][0],
            "developer": ds5[1][2][68][0],
            "description": self._extract_description(ds5[1][2]),
        }

    @staticmethod
    def _extract_description(data):
        try:
            description = data[12][0][0][1]
        except (IndexError, TypeError):
            try:
                description = data[72][0][1]
            except (IndexError, TypeError):
                description = ""

        return description.replace("<br>", "")

    def __build_app_home_url(self):
        return GOOGLE_PLAY_APP_HOME_URL.format(app_id=self.app_id)
