from .regex import *

APP_STORE_BASE_URL = "https://apps.apple.com"
APP_STORE_API_BASE_URL = "https://amp-api.apps.apple.com"
APP_STORE_APP_HOME_URL = f"{APP_STORE_BASE_URL}/us/app/{{app_slug}}/id{{app_id}}"
APP_STORE_APP_REVIEWS_URL = (
    f"{APP_STORE_API_BASE_URL}/v1/catalog/us/apps/{{app_id}}/reviews"
)
