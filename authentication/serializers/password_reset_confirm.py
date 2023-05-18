from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers

User = get_user_model()


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField()
    new_password_confirm = serializers.CharField()

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise serializers.ValidationError(
                {"non_field_errors": ["Passwords do not match."]}
            )

        try:
            uid = urlsafe_base64_decode(attrs["uid"])
            user = User.objects.get(pk=uid)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError({"uid": ["This field is not valid."]})

        if not default_token_generator.check_token(user, attrs["token"]):
            raise serializers.ValidationError({"token": ["This field is not valid."]})

        attrs["user"] = user
        return attrs

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value
