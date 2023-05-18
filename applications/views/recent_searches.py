from rest_framework.generics import ListAPIView

from applications.serializers.application import ApplicationSerializer


class RecentSearchesView(ListAPIView):
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        return self.request.user.searched_applications.order_by(
            "-searchhistory__created_at"
        ).distinct()[:10]
