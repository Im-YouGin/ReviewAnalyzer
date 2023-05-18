from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.tasks import q_email_user

User = get_user_model()


class PasswordResetView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def post(self, request):
        user = get_object_or_404(User, email=request.data.get("email"))

        subject = "Password Reset"
        message = render_to_string(
            "authentication/password_reset.html",
            {
                "email": user.email,
                "base_url": settings.FRONTEND_BASE_URL,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user),
            },
        )

        q_email_user.delay(str(user.id), subject, message)

        return Response({"detail": "Password reset email has been sent."})
