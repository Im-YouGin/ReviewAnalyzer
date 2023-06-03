from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models.email_confirmation_token import EmailConfirmationToken


class EmailConfirmView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def post(self, request):
        token = self._get_token()

        token_obj = EmailConfirmationToken.objects.filter(
            token=token, expires_at__gt=timezone.now()
        ).first()
        if not token_obj:
            raise ValidationError(
                {"non_field_errors": ["Token is invalid or expired."]}
            )

        user = token_obj.user
        user.is_active = True
        user.save()

        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})

    def _get_token(self):
        token = self.request.data.get("token")
        if not token:
            raise ValidationError({"token": ["This field is required."]})

        return token
