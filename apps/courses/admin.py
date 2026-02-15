from django.contrib import admin
from .models import Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("order", "title", "module", "activity_type", "xp")
    list_display_links = ("title",)

    # Allow quick edits from the list view
    list_editable = ("order", "module", "activity_type", "xp")

    list_filter = ("module", "activity_type")
    search_fields = ("title",)

    ordering = ("module", "order")

    fields = (
        "title",
        "module",          # ✅ THIS WAS MISSING
        "content",
        "youtube_url",
        "order",
        "xp",
        "activity_type",
        "activity_json",
    )
