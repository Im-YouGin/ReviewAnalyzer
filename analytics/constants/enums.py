from common.constants import ChoicesEnum


class Sentiment(str, ChoicesEnum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
