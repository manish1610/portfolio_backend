from django.contrib import admin
from api_v1.models import Comment


def truncate(s: str, n: int) -> str:
    """Truncate a string to `n` characters using an allipsis (...) if necessary."""
    assert n > 3, "Truncated length must be longer than the length of ellipsis '...'"
    return s if (len(s) <= n) else s[: (n - 3)] + "..."


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("added_by", "description", "date_created", "date_modified")
    search_fields = ("added_by",)

    def get_description(self, obj):
        return truncate(obj.description, 64)
