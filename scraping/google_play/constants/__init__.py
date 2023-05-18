from .enums import *

GOOGLE_PLAY_BASE_URL = "https://play.google.com"
GOOGLE_PLAY_APP_HOME_URL = (
    f"{GOOGLE_PLAY_BASE_URL}/store/apps/details?id={{app_id}}&hl=en&gl=US"
)
GOOGLE_PLAY_APP_REVIEWS_URL = (
    f"{GOOGLE_PLAY_BASE_URL}/_/PlayStoreUi/data/batchexecute?hl=en&gl=US"
)

NULL = "null"
