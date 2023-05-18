from django.conf import settings
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from authentication.models.email_confirmation_token import EmailConfirmationToken
from authentication.serializers.user import UserSerializer
from authentication.tasks import q_email_user

User = get_user_model()


class SignupView(CreateAPIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()

        # Deactivate user until the email is confirmed
        user.is_active = False
        user.save()

        confirmation_token = EmailConfirmationToken.objects.create(user=user)

        subject = "Confirm your email"
        message = render_to_string(
            "authentication/email_confirm.html",
            {
                "email": user.email,
                "base_url": settings.FRONTEND_BASE_URL,
                "token": confirmation_token.token,
            },
        )

        q_email_user.delay(str(user.id), subject, message)
