from django.urls import path, include
from .views import TasksAssignedToMeView, TaskCreateView, TasksForReviewsView, TaskDetailView, TaskDetailCommentsView, TaskDetailCommentDeleteView

urlpatterns = [
    path(
        'tasks/assigned-to-me/',
        TasksAssignedToMeView.as_view(),
        name='tasks-assigned-to-me-list'
    ),
    path(
        'tasks/reviewing/',
        TasksForReviewsView.as_view(),
        name='tasks-reviewing-list'
    ),
    path(
        'tasks/',
        TaskCreateView.as_view(),
        name='task-create-view'
    ),
    path(
        'tasks/<int:pk>/',
        TaskDetailView.as_view(),
        name='task-detail-view'
    ),
    path(
        'tasks/<int:pk>/comments/',
        TaskDetailCommentsView.as_view(),
        name='task-detail-comments-view'
    ),
    path(
        "tasks/<int:task_id>/comments/<int:comment_id>/",
        TaskDetailCommentDeleteView.as_view(),
        name="task-comment-delete",
    ),
]
