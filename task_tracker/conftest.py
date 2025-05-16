import pytest


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
def another_user_data(test_login_credentials) -> dict[str, str]:
    return {
        "email": "second@example.com",
        "password": "anotherpassword123",
        "username": "anotheruser",
        "first_name": "Another",
        "last_name": "User",
    }


@pytest.fixture
@pytest.mark.django_db
def test_user(django_user_model, test_user_data):
    return django_user_model.objects.create_user(**test_user_data)
