import re

GOOGLE_PLAY_SCRIPT_REGEX = re.compile(r"AF_initDataCallback[\s\S]*?</script")
GOOGLE_PLAY_DATA_KEY_REGEX = re.compile(r"(ds:.*?)'")
GOOGLE_PLAY_DATA_VALUE_REGEX = re.compile(r"data:([\s\S]*?), sideChannel: {}}\);</")
GOOGLE_PLAY_REVIEWS_REGEX = re.compile(r"\)]}'\n\n([\s\S]+)")
