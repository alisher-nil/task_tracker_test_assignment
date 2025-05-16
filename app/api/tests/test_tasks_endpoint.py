from typing import Generator

import pytest
from django.urls import reverse
from rest_framework import status

from tasks.models import Task


class TestTasks:
    """Test class for testing task-related endpoints."""

    tasks_url: str = reverse("api:tasks-list")

    @pytest.fixture
    def assert_no_task_created(self, django_user_model) -> Generator[None, None]:
        initial_count = Task.objects.count()
        yield
        assert Task.objects.count() == initial_count, (
            "Task is created in db with invalid data"
        )

    def test_create_task(self, authorized_client, test_user, task_data):
        """Test task creation with valid data."""
        response = authorized_client.post(self.tasks_url, data=task_data)
        assert response.status_code == status.HTTP_201_CREATED

        assert response.data["title"] == task_data["title"]
        assert response.data["description"] == task_data["description"]
        assert response.data["completed"] is task_data["completed"]

        assert "id" in response.data
        assert "created_at" in response.data
        assert "updated_at" in response.data
        assert response.data["owner"]["id"] == test_user.id

    @pytest.mark.usefixtures("assert_no_task_created")
    def test_unauthorized_create_task(self, client, task_data):
        """Test task creation without authentication."""
        response = client.post(self.tasks_url, data=task_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.usefixtures("assert_no_task_created")
    def test_missing_title(self, authorized_client, task_data):
        """Test task creation with missing title."""
        incomplete_data = task_data.copy()
        incomplete_data.pop("title")
        response = authorized_client.post(self.tasks_url, data=incomplete_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "title" in response.data

    @pytest.mark.parametrize(
        "missing_field",
        ["description", "completed"],
    )
    def test_missing_optional_fields(self, missing_field, authorized_client, task_data):
        """Test task creation with missing optional fields."""
        incomplete_data = task_data.copy()
        incomplete_data.pop(missing_field)
        response = authorized_client.post(self.tasks_url, data=incomplete_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert bool(response.data[missing_field]) is False

    def test_list_tasks(self, authorized_client, test_user):
        """Test listing tasks."""
        response = authorized_client.get(self.tasks_url)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data["results"], list)

    def test_get_task(self):
        """Test retrieving a task."""
        pass

    def test_update_task(self):
        """Test updating a task."""
        pass

    def test_delete_task(self):
        """Test deleting a task."""
        pass
