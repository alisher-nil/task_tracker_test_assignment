from django.contrib import admin

from tasks.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin interface for the Task model."""

    list_display = ("title", "owner", "created_at", "updated_at", "completed")
    list_filter = ("completed", "created_at", "updated_at", "owner")
    search_fields = ("title", "description", "owner__username")
    date_hierarchy = "created_at"

    fieldsets = (
        (None, {"fields": ("title", "description")}),
        ("Status", {"fields": ("completed",)}),
        ("Ownership", {"fields": ("owner",)}),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    readonly_fields = ("created_at", "updated_at")

    def get_queryset(self, request):
        """Optimize query by prefetching related owner."""
        return super().get_queryset(request).select_related("owner")
