from rest_framework.exceptions import ValidationError

from common.constants import MARKET_APP_URL_REGEX, MARKET_URL_MATCH_PROCESSOR, AppMarket


def parse_app_url(url):
    if not url:
        raise ValidationError({"url": ["This field is required."]})

    for market in AppMarket:
        if match := MARKET_APP_URL_REGEX[market].match(url):
            try:
                return {
                    **MARKET_URL_MATCH_PROCESSOR[market](match),
                    "market": market,
                }
            except IndexError:
                pass

    raise ValidationError({"url": ["This field is not valid."]})
