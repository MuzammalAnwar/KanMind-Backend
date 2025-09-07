from rest_framework import serializers
from kanban_app.models import Board
from kanban_app.api.serializers import UserMiniSerializer
from tasks_app.models import Task, Comment
from django.contrib.auth import get_user_model

User = get_user_model()


class TasksAssignedToMeSerializer(serializers.ModelSerializer):
    comments_count = serializers.SerializerMethodField()

    assignee = UserMiniSerializer()

    reviewer = UserMiniSerializer()

    class Meta:
        model = Task
        fields = [
            'id',
            'board',
            'title',
            'description',
            'status',
            'priority',
            'assignee',
            'reviewer',
            'due_date',
            'comments_count'
        ]

    def get_comments_count(self, obj):
        return obj.comments.count()


class TasksCreateSerializer(serializers.ModelSerializer):
    assignee = UserMiniSerializer(read_only=True)

    reviewer = UserMiniSerializer(read_only=True)

    assignee_id = serializers.PrimaryKeyRelatedField(
        source='assignee', queryset=User.objects.all(), write_only=True, required=False
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        source='reviewer', queryset=User.objects.all(), write_only=True, required=False
    )

    comments_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'board',
            'title',
            'description',
            'status',
            'priority',
            'assignee',
            'reviewer',
            'assignee_id',
            'reviewer_id',
            'due_date',
            'comments_count'
        ]

    def get_comments_count(self, obj):
        return obj.comments.count()


class TaskDetailSerializer(TasksCreateSerializer):
    board = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'board',
            'title',
            'description',
            'status',
            'priority',
            'assignee',
            'reviewer',
            'assignee_id',
            'reviewer_id',
            'due_date',
            'comments_count'
        ]


class TaskDetailCommentsSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']
        
    def get_author(self, obj):
           return f"{obj.author.first_name} {obj.author.last_name}".strip()