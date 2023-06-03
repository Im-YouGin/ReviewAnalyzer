from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "password", "password_confirm")
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": ["Passwords do not match."]}
            )
        return data

    def create(self, validated_data):
        validated_data.pop("password_confirm")

        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)

        return user
