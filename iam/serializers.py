# lib imports
from rest_framework import serializers
from django.contrib.auth import get_user_model

USER = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        data["username"] = data.get("username").lower()
        return data
