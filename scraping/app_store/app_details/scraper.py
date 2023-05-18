from bs4 import BeautifulSoup

from common.constants import GET
from scraping.app_store.constants import APP_STORE_APP_HOME_URL
from scraping.common.app_details import BaseAppDetailsScraper


class AppStoreAppDetailsScraper(BaseAppDetailsScraper):
    def __init__(self, app_id: str, app_slug: str):
        super().__init__()

        self.app_id = app_id
        self.app_slug = app_slug

        self.__app_home_url = self.__build_app_home_url()

    def get_details(self):
        response = self._request(self.__app_home_url, method=GET)
        soup = BeautifulSoup(response.content, "lxml")

        return self._parse_details(soup)

    def _parse_details(self, soup):
        return {
            "name": soup.select_one(".app-header__title").text.strip().split("\n")[0],
            "developer": soup.select_one(".app-header__identity a.link").text.strip(),
            "description": soup.select_one(".section__description").text.strip(),
        }

    def __build_app_home_url(self):
        return APP_STORE_APP_HOME_URL.format(app_slug=self.app_slug, app_id=self.app_id)
