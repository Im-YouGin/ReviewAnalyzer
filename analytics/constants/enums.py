from enum import Enum

from common.constants import ChoicesEnum


class Sentiment(str, ChoicesEnum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class Color(str, Enum):
    POSITIVE = "#01b51c"
    NEUTRAL = "#8676fe"
    NEGATIVE = "#fbb96c"
