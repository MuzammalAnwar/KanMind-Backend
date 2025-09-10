from django.db import models
from kanban_app.models import Board
from django.conf import settings

# Create your models here.


class Task(models.Model):
    class Status(models.TextChoices):
        TODO = "to-do"
        IN_PROGRESS = "in-progress"
        REVIEW = "review"
        DONE = "done"

    class Priority(models.TextChoices):
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"

    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    
    title = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO,
        db_index=True,
    )

    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        db_index=True,
    )

    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="assigned_tasks",
    )
    
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="review_tasks",
    )

    due_date = models.DateField(null=True, blank=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="created_tasks",
        db_index=True,
    )

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["board", "status"]),
            models.Index(fields=["board", "priority"]),
        ]

    def __str__(self):
        return f"{self.title} [{self.status}]"


class Comment(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    
    content = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"Comment by {self.author} on {self.task}"
