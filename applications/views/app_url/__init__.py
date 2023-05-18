from rest_framework import views
from rest_framework.response import Response
from rest_framework.views import APIView

from applications.serializers.application import ApplicationSerializer
from applications.utils.validators import parse_app_url
from common.constants import AppMarket

from .strategy import AppStoreAppUrlStrategy, GooglePlayAppUrlStrategy


class AppUrlView(APIView):
    _strategies = {
        AppMarket.APP_STORE: AppStoreAppUrlStrategy,
        AppMarket.GOOGLE_PLAY: GooglePlayAppUrlStrategy,
    }

    def post(self, request):
        app_identifiers = self._get_app_identifiers_from_url()

        market = app_identifiers.pop("market")
        strategy_cls = self._strategies.get(market)
        app_obj, created = strategy_cls(app_identifiers).process()

        self.request.user.searched_applications.add(app_obj)

        return Response({"id": app_obj.id, "is_new": created})

    def _get_app_identifiers_from_url(self):
        app_url = self.request.data.get("url")
        return parse_app_url(app_url)
