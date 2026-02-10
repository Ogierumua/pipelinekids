from django.contrib import admin
from .models import Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("order", "title", "activity_type", "xp")

    # ✅ keep the row clickable using "title"
    list_display_links = ("title",)

    # ✅ now order can be editable
    list_editable = ("order", "activity_type", "xp")

    ordering = ("order",)

    fields = (
        "title",
        "content",
        "youtube_url",
        "order",
        "xp",
        "activity_type",
        "activity_json",
    )


