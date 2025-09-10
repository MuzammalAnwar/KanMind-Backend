from django.contrib import admin
from .models import Task, Comment


class CommentInline(admin.TabularInline):
    """
    Manage comments directly inside the Task admin page.
    """
    model = Comment
    extra = 1
    autocomplete_fields = ["author"]
    readonly_fields = ("created_at",)
    show_change_link = True


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id", "title", "board", "status", "priority",
        "assignee", "reviewer", "due_date", "created_at",
    )
    list_display_links = ("id", "title")
    search_fields = (
        "title",
        "description",
        "assignee__username",
        "reviewer__username",
        "board__title",
    )
    list_filter = ("status", "priority", "due_date", "board")
    ordering = ("-created_at",)
    autocomplete_fields = ["board", "assignee", "reviewer"]
    date_hierarchy = "due_date"
    inlines = [CommentInline]
    readonly_fields = ("created_at",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "task", "author", "short_content", "created_at")
    list_display_links = ("id", "task")
    search_fields = (
        "content",
        "author__username",
        "author__first_name",
        "author__last_name",
        "task__title",
    )
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    autocomplete_fields = ["task", "author"]
    readonly_fields = ("created_at",)

    @admin.display(description="Content")
    def short_content(self, obj):
        return obj.content[:50] + ("..." if len(obj.content) > 50 else "")
