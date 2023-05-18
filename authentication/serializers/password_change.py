from django.contrib.auth import password_validation
from rest_framework import serializers


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct.")

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
