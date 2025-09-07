from django.urls import path, include
from .views import TasksAssignedToMeView, TaskCreateView, TasksForReviewsView, TaskDetailView

urlpatterns = [
    path('tasks/assigned-to-me/', TasksAssignedToMeView.as_view(),
         name='tasks-assigned-to-me-list'),
    path('tasks/reviewing/', TasksForReviewsView.as_view(),
         name='tasks-reviewing-list'),
    path('tasks/', TaskCreateView.as_view(),
         name='task-create-view'),
    path('tasks/<int:pk>', TaskDetailView.as_view(),
         name='task-detail-view'),
]
