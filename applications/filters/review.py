import django_filters
from django_filters import rest_framework as filters
from django_filters.widgets import CSVWidget

from analytics.constants.enums import Sentiment
from applications.models import Review
from common.constants import AppMarket, Star


class ReviewFilter(filters.FilterSet):
    stars = django_filters.MultipleChoiceFilter(
        choices=Star.choices(), widget=CSVWidget
    )
    sentiment = django_filters.MultipleChoiceFilter(
        choices=Sentiment.choices(), field_name="sentiment_str", widget=CSVWidget
    )
    market = django_filters.MultipleChoiceFilter(
        choices=AppMarket.choices(), widget=CSVWidget
    )
    date_range = django_filters.DateFromToRangeFilter(field_name="source_created_at")

    class Meta:
        model = Review
        fields = ["stars", "sentiment_str", "market", "source_created_at"]
