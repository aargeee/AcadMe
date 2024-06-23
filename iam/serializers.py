# lib imports
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from iam.models import AppUser

from rest_framework_simplejwt.tokens import RefreshToken

USER = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        data["username"] = data.get("username").lower()
        return data

class TutorSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ["username", "first_name", "last_name", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = AppUser(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            role=AppUser.ROLES.TUTOR,
            is_staff=False,
            is_active=True,
        )
        user.set_password(validated_data["password"])
        user.save()

        # Clear any default groups and add user to 'tutor' group
        user.groups.clear()
        group = Group.objects.get(name="tutor")
        user.groups.add(group)

        return user


class LearnerSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ["username", "first_name", "last_name", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = AppUser(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            role=AppUser.ROLES.LEARNER,
            is_staff=False,
            is_active=True,
        )
        user.set_password(validated_data["password"])
        user.save()

        user.groups.clear()
        group = Group.objects.get(name="learner")
        user.groups.add(group)

        # Clear any default groups and add user to 'learner' group
        return user

class TutorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER
        fields = ["id", "username", "first_name", "last_name"]
        