from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from authentication.serializers.password_reset_confirm import (
    PasswordResetConfirmSerializer,
)


class PasswordResetConfirmView(GenericAPIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        new_password = serializer.validated_data["new_password"]
        user.set_password(new_password)
        user.save()

        return Response({"detail": "Password has been reset with the new password."})
