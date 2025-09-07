from django.db.models import Count, Q
from rest_framework import generics, permissions, mixins
from kanban_app.models import Board
from tasks_app.models import Task, Comment
from .serializers import TasksAssignedToMeSerializer, TasksCreateSerializer, TaskDetailSerializer, TaskDetailCommentsSerializer
from rest_framework.exceptions import PermissionDenied, ValidationError
from kanban_app.api.permissions import IsBoardMember
from django.shortcuts import get_object_or_404
from .permissions import IsCommentAuthor


class TasksAssignedToMeView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TasksAssignedToMeSerializer

    def get_queryset(self):
        u = self.request.user
        qs = Task.objects.filter(assignee=u)

        params = self.request.query_params
        status_ = params.get("status")
        if status_:
            qs = qs.filter(status=status_)

        board_id = params.get("board")
        if board_id:
            qs = qs.filter(board_id=board_id)

        return qs.distinct()


class TasksForReviewsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TasksAssignedToMeSerializer

    def get_queryset(self):
        u = self.request.user
        qs = Task.objects.filter(reviewer=u)

        params = self.request.query_params
        status_ = params.get("status")
        if status_:
            qs = qs.filter(status=status_)

        board_id = params.get("board")
        if board_id:
            qs = qs.filter(board_id=board_id)

        return qs.distinct()


class TaskCreateView(generics.CreateAPIView):
    serializer_class = TasksCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Task.objects.all()

    def perform_create(self, serializer):
        u = self.request.user
        board = serializer.validated_data["board"]
        if not board.members.filter(pk=u.pk).exists():
            raise PermissionDenied(
                "Only board members can create tasks on this board.")
        assignee = serializer.validated_data.get("assignee")
        reviewer = serializer.validated_data.get("reviewer")
        member_ids = set(board.members.values_list("id", flat=True))
        errors = {}
        if assignee and assignee.id not in member_ids:
            errors["assignee_id"] = "Assignee must be a member of this board."
        if reviewer and reviewer.id not in member_ids:
            errors["reviewer_id"] = "Reviewer must be a member of this board."
        if errors:
            raise ValidationError(errors)
        serializer.save()


class TaskDetailView(mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     generics.GenericAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["patch", "delete", "options"]

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_update(self, serializer):
        instance = self.get_object()
        target_board = serializer.validated_data.get("board", instance.board)
        user = self.request.user
        if not target_board.members.filter(pk=user.pk).exists():
            raise PermissionDenied(
                "Only board members can update tasks on this board.")
        effective_assignee = serializer.validated_data.get(
            "assignee", instance.assignee)
        effective_reviewer = serializer.validated_data.get(
            "reviewer", instance.reviewer)
        member_ids = set(target_board.members.values_list("id", flat=True))
        errors = {}
        if effective_assignee and effective_assignee.id not in member_ids:
            errors["assignee_id"] = "Assignee must be a member of the target board."
        if effective_reviewer and effective_reviewer.id not in member_ids:
            errors["reviewer_id"] = "Reviewer must be a member of the target board."
        if errors:
            raise ValidationError(errors)
        serializer.save()


class TaskDetailCommentsView(generics.ListCreateAPIView):
    serializer_class = TaskDetailCommentsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_task(self):
        task = get_object_or_404(Task, pk=self.kwargs["pk"])
        user = self.request.user
        board = task.board
        is_member = board.members.filter(id=user.id).exists()
        if not is_member:
            raise PermissionDenied(
                "Only board members can view or comment on this task.")
        return task

    def get_queryset(self):
        return Comment.objects.filter(task=self.get_task()).select_related("author")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, task=self.get_task())


class TaskDetailCommentDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsCommentAuthor]
    lookup_url_kwarg = "comment_id"
    queryset = Comment.objects.all()

    def get_queryset(self):
        get_object_or_404(Task, pk=self.kwargs["task_id"])
        return Comment.objects.filter(task_id=self.kwargs["task_id"])
