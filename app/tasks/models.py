from django.contrib.auth import get_user_model
from django.db import models

from task_tracker.constants import TITLE_FIELD_MAX_LENGTH

User = get_user_model()


class Task(models.Model):
    """Model representing a task in the task tracker application."""

    title = models.CharField(max_length=TITLE_FIELD_MAX_LENGTH)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False, db_index=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self) -> str:
        return self.title
