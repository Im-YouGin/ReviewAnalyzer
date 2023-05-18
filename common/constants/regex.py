import re

APP_STORE_URL_REGEX = re.compile(
    r"^https://apps\.apple\.com/\w{2}/app/([\w-]+)/id(\d+)"
)
GOOGLE_PLAY_URL_REGEX = re.compile(
    r"^https://play\.google\.com/store/apps/details\?id=([\w\.]+)"
)
