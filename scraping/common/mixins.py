import requests
from fake_useragent import UserAgent
from requests.adapters import HTTPAdapter
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_404_NOT_FOUND
from urllib3 import Retry

from common.constants import GET


class RequestsMixin:
    _session: requests.Session

    _ua = UserAgent()

    def _request(self, url, method: str = GET, **kwargs):
        method_caller = getattr(self._session, method.lower())
        response = method_caller(url, **kwargs)
        if response.status_code == HTTP_404_NOT_FOUND:
            raise NotFound({"url": ["No application found at the provided URL."]})

        return response

    def _create_session(self):
        session = requests.Session()
        session.headers.update({"User-Agent": self._ua.random})
        session.mount(
            "https://",
            HTTPAdapter(
                max_retries=Retry(
                    total=5,
                    backoff_factor=1,
                    status_forcelist=[429, 500, 502, 503, 504],
                )
            ),
        )

        return session
