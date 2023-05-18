from rest_framework.generics import RetrieveAPIView

from applications.models import Application
from applications.serializers.application import ApplicationSerializer


class ApplicationView(RetrieveAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
