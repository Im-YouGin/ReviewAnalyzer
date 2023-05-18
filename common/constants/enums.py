from enum import Enum


class ChoicesEnum(Enum):
    @classmethod
    def choices(cls):
        return [(x.value, x.name.replace("_", " ").title()) for x in cls]


class AppMarket(str, ChoicesEnum):
    APP_STORE = "app_store"
    GOOGLE_PLAY = "google_play"

    @property
    def pretty(self):
        return " ".join(word.capitalize() for word in self.value.split("_"))


class AppStatus(str, ChoicesEnum):
    READY = "ready"
    UPDATING = "updating"


class Star(int, ChoicesEnum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
