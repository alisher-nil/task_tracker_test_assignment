from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class EmailTokenObtainSerializer(TokenObtainPairSerializer):
    """
    Custom serializer for JWT token generation using email and password.
    """

    @classmethod
    def get_token(cls, user):
        """
        Generate a JWT token for the given user.
        """
        token = super().get_token(user)
        token["email"] = user.email
        return token


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
        extra_kwargs = {
            "email": {"required": True},
        }

    def create(self, validated_data):
        """
        Create a new user with the provided validated data.
        """
        user = User.objects.create_user(**validated_data)
        return user
