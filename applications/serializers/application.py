from rest_framework import serializers

from applications.models.application import Application


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ("id", "name", "description")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["status"] = instance.status

        return representation
