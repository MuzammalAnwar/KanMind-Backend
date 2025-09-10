from rest_framework import serializers
from kanban_app.models import Board
from tasks_app.models import Task
from django.contrib.auth import get_user_model

User = get_user_model()


class BoardSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(source="owner.id", read_only=True)

    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, write_only=True, required=False
    )

    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = [
            'id',
            'title',
            'member_count',
            'ticket_count',
            'tasks_to_do_count',
            'tasks_high_prio_count',
            'owner_id', 'members'
        ]

    def create(self, validated_data):
        members = validated_data.pop("members", [])
        user = self.context["request"].user

        board = Board.objects.create(owner=user, **validated_data)

        members = list(members)  # make sure it's a list
        if members:
            board.members.add(*members)

        return board

    def get_member_count(self, obj):
        return obj.members.count()

    def get_ticket_count(self, obj):
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status="to-do").count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority="high").count()


class UserMiniSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

    def get_fullname(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


class TaskMiniSerializer(serializers.ModelSerializer):
    assignee = UserMiniSerializer(read_only=True)

    reviewer = UserMiniSerializer(read_only=True)

    comments_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
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


class BoardDetailSerializer(BoardSerializer):
    # disable aggregated fields from parent
    member_count = None
    ticket_count = None
    tasks_to_do_count = None
    tasks_high_prio_count = None

    # write members by ids, read members as objects
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, required=False, write_only=True
    )
    members_data = UserMiniSerializer(
        source="members", many=True, read_only=True)

    # add owner_data for PATCH response
    owner_data = UserMiniSerializer(source="owner", read_only=True)

    tasks = TaskMiniSerializer(read_only=True, many=True)

    class Meta(BoardSerializer.Meta):
        fields = [
            "id",
            "title",
            "owner_id",      # default (non-PATCH) returns owner_id
            "owner_data",    # only exposed on PATCH
            "members",
            "tasks",
            "members_data",
        ]

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.save()

        if "members" in validated_data:
            new_members = validated_data["members"]
            instance.members.set(new_members)

        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # handle members: swap between 'members' and 'members_data'
        members_nested = data.pop("members_data", [])
        # handle owner: switch owner_id -> owner_data for PATCH only
        owner_nested = data.pop("owner_data", None)

        req = self.context.get("request")
        if req and req.method.upper() == "PATCH":
            # For PATCH: return detailed members + detailed owner
            data["members_data"] = members_nested
            if owner_nested is not None:
                data["owner_data"] = owner_nested
            # Remove owner_id on PATCH
            data.pop("owner_id", None)
            data.pop("tasks", None)
        else:
            # For non-PATCH: keep owner_id and expose members as array of users (under 'members')
            data["members"] = members_nested
            # Ensure owner_data is not present on non-PATCH
            data.pop("owner_data", None)

        return data