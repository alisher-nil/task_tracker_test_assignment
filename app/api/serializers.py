from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken

from tasks.models import Task

User = get_user_model()


# Since the assignment expects only one endpoint for login,
# without refresh token, a custom serializer returns only the access token.
class SimpleTokenObtainSerializer(TokenObtainSerializer):
    token_class = AccessToken

    def validate(self, attrs: dict[str, Any]) -> dict[str, str]:
        data = super().validate(attrs)
        token = self.get_token(self.user)
        data["access_token"] = str(token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class UserBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer for user model.
    """

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
        )


class SignUpSerializer(UserBaseSerializer):
    """
    Serializer for user registration.
    """

    password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password],
    )

    class Meta:
        model = User
        fields = UserBaseSerializer.Meta.fields + ("password",)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class TasksSerializer(serializers.ModelSerializer):
    """
    Serializer for task model.
    """

    owner = UserBaseSerializer(read_only=True)

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
            "completed",
            "owner",
        )
        read_only_fields = ("id", "created_at", "updated_at", "owner")
