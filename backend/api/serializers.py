from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user

class SecretsSerializer(serializers.Serializer):
    name = serializers.CharField()
    value = serializers.CharField()

class TransalationRequestSerializer(serializers.Serializer):
    text = serializers.CharField()
    operation = serializers.CharField()
    key = serializers.CharField(required=False)

class TransalationResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    text = serializers.CharField()