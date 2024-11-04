from django.contrib.auth.models import User
from rest_framework import serializers

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

class GithubRetriggerAction(serializers.Serializer):
    event = serializers.CharField()
    repository = serializers.CharField()