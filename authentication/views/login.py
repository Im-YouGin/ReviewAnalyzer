from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from authentication.serializers.login import LoginSerializer

User = get_user_model()


class LoginView(GenericAPIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)

        return Response({"token": token.key})
