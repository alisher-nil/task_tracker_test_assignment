import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from api.tests.helpers.utils import bad_user_creation_count_assertion

User = get_user_model()


@pytest.mark.django_db
def test_user_creation(client, test_user_data):
    url = reverse("api:register")
    response = client.post(url, data=test_user_data)
    assert response.status_code == 201
    assert response.data["email"] == test_user_data["email"]
    assert response.data["username"] == test_user_data["username"]
    assert "password" not in response.data


@pytest.mark.usefixtures("test_user")
@bad_user_creation_count_assertion
def test_user_creation_with_existing_email(
    client,
    register_url,
    another_user_data,
    test_user_email,
):
    another_user_data["email"] = test_user_email
    response = client.post(register_url, data=another_user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data


@pytest.mark.django_db
@bad_user_creation_count_assertion
def test_user_creation_with_invalid_email(client, test_user_data, register_url):
    test_user_data["email"] = "NotAnEmail"
    response = client.post(register_url, data=test_user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data


@pytest.mark.usefixtures("test_user")
@bad_user_creation_count_assertion
def test_user_creation_with_existing_username(
    client,
    another_user_data,
    test_user_data,
    register_url,
):
    another_user_data["username"] = test_user_data["username"]
    response = client.post(register_url, data=another_user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "username" in response.data
