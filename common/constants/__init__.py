from .enums import *
from .regex import *

# Regex stuff
MARKET_APP_URL_REGEX = {
    AppMarket.APP_STORE: APP_STORE_URL_REGEX,
    AppMarket.GOOGLE_PLAY: GOOGLE_PLAY_URL_REGEX,
}

MARKET_URL_MATCH_PROCESSOR = {
    AppMarket.APP_STORE: lambda match: {
        "app_slug": match.group(1),
        "app_id": match.group(2),
    },
    AppMarket.GOOGLE_PLAY: lambda match: {
        "app_id": match.group(1),
    },
}

# Request methods
GET = "GET"
POST = "GET"

BATCH_SIZE = 2000
