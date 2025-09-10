from django.contrib import admin
from .models import BoardMember, Board


class BoardMemberInline(admin.TabularInline):
    """
    Manage board memberships right on the Board page.
    """
    model = BoardMember
    extra = 1
    autocomplete_fields = ["user"]
    verbose_name = "Member"
    verbose_name_plural = "Members"
    # Avoid huge selects
    show_change_link = True


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "member_count", "members_sample")
    list_display_links = ("id", "title")
    search_fields = (
        "title",
        "owner__username",
        "owner__first_name",
        "owner__last_name",
        "owner__email",
    )
    list_filter = ("owner",)
    ordering = ("id",)
    autocomplete_fields = ["owner"]
    inlines = [BoardMemberInline]
    readonly_fields = ("member_count",)

    @admin.display(description="Members")
    def member_count(self, obj: Board) -> int:
        return obj.members.count()

    @admin.display(description="Members (first 3)")
    def members_sample(self, obj: Board):
        names = list(
            obj.members.values_list("username", flat=True)[:3]
        )
        more = obj.members.count() - len(names)
        text = ", ".join(names) + (f" +{more}" if more > 0 else "")
        return text or "-"
