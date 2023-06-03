import logging

import pandas as pd
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response

from analytics.constants import ANALYTICS_EMPTY_RESPONSE
from analytics.manager import AnalyticsManager
from applications.filters.review import ReviewFilter
from applications.models import Application

logger = logging.getLogger("review_analyzer")


class ApplicationAnalyticsView(ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter

    def get_queryset(self):
        application = get_object_or_404(Application, id=self.kwargs["pk"])
        return application.review_set.order_by("source_created_at")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        try:
            df = self._create_dataframe(queryset)
            analytics = AnalyticsManager(df).get_analytics()

        except Exception as e:
            analytics = ANALYTICS_EMPTY_RESPONSE

            logger.exception(
                f'Exception occurred when trying to get analytics for app with pk={self.kwargs["pk"]}.\n{e}'
            )

        return Response(analytics)

    @staticmethod
    def _create_dataframe(queryset):
        df = pd.DataFrame(
            list(
                queryset.values("stars", "market", "source_created_at", "sentiment_str")
            )
        )
        df["date"] = pd.to_datetime(df.pop("source_created_at"))

        return df
