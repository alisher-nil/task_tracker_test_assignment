import datetime as dt
from typing import Generator

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.settings import api_settings

from tasks.models import Task


class TestTasks:
    """Test class for testing task-related endpoints."""

    tasks_url_path = "api:tasks-list"
    tasks_url_detail_path = "api:tasks-detail"
    model_class = Task

    @pytest.fixture
    def task_data(self) -> dict[str, str]:
        return {
            "title": "Test Task",
            "description": "This is a test task.",
            "completed": False,
        }

    @pytest.fixture
    def update_task_data(self) -> dict[str, str]:
        return {
            "title": "Updated Task",
            "description": "This is an updated test task.",
            "completed": True,
        }

    @pytest.fixture
    def test_task(self, test_user, task_data) -> Task:
        return Task.objects.create(
            title=task_data["title"],
            description=task_data["description"],
            completed=task_data["completed"],
            owner=test_user,
        )

    @pytest.fixture
    def multiple_tasks(self, test_user):
        page_size = api_settings.PAGE_SIZE
        for i in range(page_size + 1):
            self.model_class.objects.create(
                title=f"Task {i + 1}",
                description=f"Description for task {i + 1}",
                completed=False,
                owner=test_user,
            )

    @pytest.fixture
    def another_user_task(self, another_user):
        return self.model_class.objects.create(
            title="Another User's Task",
            description="This task belongs to another user.",
            completed=False,
            owner=another_user,
        )

    def test_create_task(self, authorized_client, test_user, task_data):
        """Test task creation with valid data."""
        response = authorized_client.post(reverse(self.tasks_url_path), data=task_data)
        assert response.status_code == status.HTTP_201_CREATED

        assert response.data["title"] == task_data["title"]
        assert response.data["description"] == task_data["description"]
        assert response.data["completed"] is task_data["completed"]

        assert "id" in response.data
        assert "created_at" in response.data
        assert "updated_at" in response.data
        assert response.data["owner"]["id"] == test_user.id
        assert self.model_class.objects.filter(id=response.data["id"]).exists()

    @pytest.mark.usefixtures("test_task")
    def test_list_tasks(self, authorized_client):
        """Test listing tasks."""
        response = authorized_client.get(reverse(self.tasks_url_path))
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data["results"], list)

    def test_get_task(self, test_task, authorized_client):
        """Test retrieving a task."""
        response = authorized_client.get(
            reverse(
                self.tasks_url_detail_path,
                args=[test_task.id],
            )
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == test_task.id

    def test_update_task(self, test_task, authorized_client, update_task_data):
        """Test updating a task."""
        initial_update_date = test_task.updated_at
        response = authorized_client.patch(
            reverse(self.tasks_url_detail_path, args=[test_task.id]),
            data=update_task_data,
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == update_task_data["title"]
        assert response.data["description"] == update_task_data["description"]
        assert response.data["completed"] is update_task_data["completed"]

        update_date = dt.datetime.fromisoformat(response.data["updated_at"])
        assert update_date > initial_update_date

    def test_delete_task(self, test_task, authorized_client):
        """Test deleting a task."""
        response = authorized_client.delete(
            reverse(self.tasks_url_detail_path, args=[test_task.id]),
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Task.objects.filter(id=test_task.id).exists()


@pytest.mark.django_db
class TestInvalidTaskCreation(TestTasks):
    """Test class for testing task-related endpoints with bad requests."""

    @pytest.fixture
    def assert_no_object_created(self) -> Generator[None, None]:
        initial_count = self.model_class.objects.count()
        yield
        assert self.model_class.objects.count() == initial_count, (
            "Object is created in db with invalid data"
        )

    @pytest.mark.usefixtures("assert_no_object_created")
    def test_missing_title(self, authorized_client, task_data):
        """Test task creation with missing title."""
        incomplete_data = task_data.copy()
        incomplete_data.pop("title")
        response = authorized_client.post(
            reverse(self.tasks_url_path),
            data=incomplete_data,
        )
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
        response = authorized_client.post(
            reverse(self.tasks_url_path),
            data=incomplete_data,
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert bool(response.data[missing_field]) is False


class TestListTasks(TestTasks):
    """Test class for testing task listing endpoints."""

    @pytest.mark.usefixtures("multiple_tasks")
    def test_pagination(self, authorized_client):
        """Test task listing with pagination."""
        response = authorized_client.get(reverse(self.tasks_url_path))
        objects_count = self.model_class.objects.count()
        assert response.status_code == status.HTTP_200_OK
        assert "next" in response.data
        assert "previous" in response.data
        assert isinstance(response.data["results"], list)
        assert objects_count > api_settings.PAGE_SIZE
        assert len(response.data["results"]) == api_settings.PAGE_SIZE

    @pytest.mark.usefixtures("multiple_tasks")
    def test_filters_by_title(self, authorized_client, test_task):
        """Test filtering tasks by title."""
        partial_title = test_task.title[:3]

        response = authorized_client.get(
            reverse(self.tasks_url_path),
            data={"search": partial_title},
        )
        assert self.model_class.objects.count() > 1
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data["results"], list)
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["id"] == test_task.id

    @pytest.mark.usefixtures("multiple_tasks")
    def test_filters_by_completed(self, authorized_client, test_task):
        """Test filtering tasks by completed status."""
        test_task.completed = True
        test_task.save()

        response = authorized_client.get(
            reverse(self.tasks_url_path),
            data={"completed": test_task.completed},
        )
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data["results"], list)
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["id"] == test_task.id


class TestUnauthorizedAccess(TestTasks):
    """Test class for testing unauthorized access to task-related endpoints."""

    def test_create_task_unauthorized(self, client, task_data):
        """Test unauthorized task creation."""
        response = client.post(reverse(self.tasks_url_path), data=task_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_tasks_unauthorized(self, client):
        """Test unauthorized task listing."""
        response = client.get(reverse(self.tasks_url_path))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_task_unauthorized(self, client, test_task):
        """Test unauthorized task retrieval."""
        response = client.get(reverse(self.tasks_url_detail_path, args=[test_task.id]))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_task_unauthorized(self, test_task, client, update_task_data):
        """Test unauthorized task update."""
        response = client.patch(
            reverse(self.tasks_url_detail_path, args=[test_task.id]),
            data=update_task_data,
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_replace_task_unauthorized(self, test_task, client, update_task_data):
        """Test unauthorized task update."""
        response = client.put(
            reverse(self.tasks_url_detail_path, args=[test_task.id]),
            data=update_task_data,
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_task_unauthorized(self, test_task, client):
        """Test unauthorized task deletion."""
        response = client.delete(
            reverse(self.tasks_url_detail_path, args=[test_task.id])
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestTaskPermissions(TestTasks):
    def test_cannot_edit_others_tasks(
        self,
        another_user_task,
        authorized_client,
        update_task_data,
    ):
        """Test that another user cannot update a task."""
        response = authorized_client.patch(
            reverse(self.tasks_url_detail_path, args=[another_user_task.id]),
            data=update_task_data,
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_cannot_delete_others_tasks(self, another_user_task, authorized_client):
        """Test that another user cannot delete a task."""
        response = authorized_client.delete(
            reverse(self.tasks_url_detail_path, args=[another_user_task.id])
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_user_tasks_visibility(
        self,
        authorized_client,
        another_user_task,
        test_task,
    ):
        """Test that a user can't see another user's tasks."""
        response = authorized_client.get(reverse(self.tasks_url_path))
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data["results"], list)
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["id"] == test_task.id
        assert another_user_task.id not in [
            task["id"] for task in response.data["results"]
        ]
