import pandas as pd
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response

from analytics.manager import AnalyticsManager
from applications.filters.review import ReviewFilter
from applications.models import Application, Review


class ApplicationAnalyticsView(ListAPIView):
    queryset = Review.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter

    def get_queryset(self):
        application = get_object_or_404(Application, pk=self.kwargs["pk"])
        return application.review_set.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        df = self._create_dataframe(queryset)

        analytics = AnalyticsManager(df).get_analytics()

        return Response(analytics)

    @staticmethod
    def _create_dataframe(queryset):
        df = pd.DataFrame(
            list(
                queryset.values("stars", "market", "source_created_at", "sentiment_str")
            )
        )
        df["date"] = df.pop("source_created_at").dt.date
        return df
