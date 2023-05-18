from django.contrib.auth import update_session_auth_hash
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from authentication.serializers.password_change import PasswordChangeSerializer


class PasswordChangeView(GenericAPIView):
    serializer_class = PasswordChangeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_password = serializer.validated_data["new_password"]
        request.user.set_password(new_password)
        request.user.save()

        update_session_auth_hash(request, request.user)
        return Response()
