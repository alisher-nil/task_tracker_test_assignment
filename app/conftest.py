from typing import TypeVar

import pytest
from django.contrib.auth.models import AbstractBaseUser
from django.test.client import Client
from django.utils.module_loading import import_string
from rest_framework_simplejwt.settings import api_settings

User = TypeVar("User", bound=AbstractBaseUser)


@pytest.fixture
def test_user_email() -> str:
    return "test@example.com"


@pytest.fixture
def test_user_password() -> str:
    return "testpassword123"


@pytest.fixture
def test_login_credentials(test_user_email, test_user_password) -> dict[str, str]:
    return {
        "email": test_user_email,
        "password": test_user_password,
    }


@pytest.fixture
def test_user_data(test_login_credentials) -> dict[str, str]:
    return {
        **test_login_credentials,
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
    }


@pytest.fixture
def another_user_data() -> dict[str, str]:
    return {
        "email": "second@example.com",
        "password": "anotherpassword123",
        "username": "anotheruser",
        "first_name": "Another",
        "last_name": "User",
    }


@pytest.fixture
def test_user(django_user_model, test_user_data) -> User:
    return django_user_model.objects.create_user(**test_user_data)


@pytest.fixture
def authentication_token(test_user) -> str:
    TokenSerializer = import_string(api_settings.TOKEN_OBTAIN_SERIALIZER)
    return TokenSerializer.get_token(test_user)


@pytest.fixture
def authorized_client(client, authentication_token) -> Client:
    client.defaults["HTTP_AUTHORIZATION"] = f"Bearer {authentication_token}"
    return client


@pytest.fixture
def task_data() -> dict[str, str]:
    return {
        "title": "Test Task",
        "description": "This is a test task.",
        "completed": False,
    }
