import pytest
from django.contrib.auth import get_user_model
from django.test.client import Client
from django.urls import reverse
from rest_framework import status

User = get_user_model()


@pytest.fixture
def setup_test_user_creation_class(request, client, test_user_data):
    request.cls.client = client
    request.cls.user_data = test_user_data


@pytest.mark.django_db
@pytest.mark.usefixtures("setup_test_user_creation_class")
class TestUserCreation:
    register_url: str = reverse("api:register")
    client: Client
    user_data: dict[str, str]

    def test_user_creation(self):
        """Test user creation with valid data."""

        response = self.client.post(self.register_url, data=self.user_data)
        assert response.status_code == 201
        assert response.data["email"] == self.user_data["email"]
        assert response.data["username"] == self.user_data["username"]
        assert "password" not in response.data

    @pytest.mark.usefixtures("test_user", "assert_no_user_created")
    @pytest.mark.parametrize(
        "existing_field",
        ["email", "username"],
    )
    def test_existing_credentials(self, existing_field, another_user_data):
        """Test user creation with existing email or username."""

        another_user_data[existing_field] = self.user_data[existing_field]
        response = self.client.post(self.register_url, data=another_user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert existing_field in response.data

    @pytest.mark.usefixtures("assert_no_user_created")
    @pytest.mark.parametrize(
        "missing_field",
        ["email", "username", "password"],
    )
    def test_missing_fields(self, missing_field):
        """Test user creation with missing fields."""

        user_data = self.user_data.copy()
        user_data.pop(missing_field)
        response = self.client.post(self.register_url, data=user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert missing_field in response.data

    @pytest.mark.parametrize(
        "email",
        ["", "invalidemail.com", "user@.com", "NotAnEmail"],
    )
    @pytest.mark.usefixtures("assert_no_user_created")
    def test_user_creation_with_invalid_email(self, email):
        """Test user creation with invalid email."""

        self.user_data["email"] = email
        response = self.client.post(self.register_url, data=self.user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data

    @pytest.mark.parametrize(
        "password",
        ["", "short", "123", "password"],
    )
    @pytest.mark.usefixtures("assert_no_user_created")
    def test_user_creation_with_invalid_password(self, password):
        """Test user creation with invalid password."""

        self.user_data["password"] = password
        response = self.client.post(self.register_url, data=self.user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password" in response.data


@pytest.fixture
def setup_login_test_class(request, client, test_login_credentials):
    """Fixture to set up the test class with client and user credentials."""
    request.cls.client = client
    request.cls.user_credentials = test_login_credentials


@pytest.mark.django_db
@pytest.mark.usefixtures("setup_login_test_class", "test_user")
class TestUserLogin:
    login_url: str = reverse("api:login")
    tasks_url: str = reverse("api:tasks-list")
    client: Client
    user_credentials: dict[str, str]

    def test_user_login(self):
        """Test user login with valid credentials."""

        response = self.client.post(self.login_url, data=self.user_credentials)
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.data
        token = response.data["access_token"]
        assert len(token.split(".")) == 3

    def test_invalid_credentials(self):
        """Test login with invalid credentials."""

        invalid_credentials = {
            "email": "invalid@example.com",
            "password": "wrongpassword",
        }
        response = self.client.post(self.login_url, data=invalid_credentials)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "detail" in response.data

    @pytest.mark.parametrize(
        "missing_field",
        ["email", "password"],
    )
    def test_missing_credentials(self, missing_field):
        """Test missing credentials during login."""

        credentials = self.user_credentials.copy()
        credentials.pop(missing_field)
        response = self.client.post(self.login_url, data=credentials)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert missing_field in response.data

    def test_token_authentication(self):
        """Test token authentication for accessing protected endpoints."""

        # Attempt to access the tasks endpoint without authentication
        response = self.client.get(self.tasks_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        # Authenticate the user
        response = self.client.post(self.login_url, data=self.user_credentials)
        token = response.data["access_token"]
        # Use the token to access the tasks endpoint
        response = self.client.get(self.tasks_url, HTTP_AUTHORIZATION=f"Bearer {token}")
        assert response.status_code == status.HTTP_200_OK
