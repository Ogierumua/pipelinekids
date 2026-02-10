from django.db import models
import re


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    youtube_url = models.URLField(blank=True, null=True)
   
    order = models.PositiveIntegerField()
    xp = models.PositiveIntegerField(default=10)

    activity_type = models.CharField(
        max_length=20,
        choices=[
            ("none", "None"),
            ("order", "Order Blocks"),
            ("choice", "Choice Cards"),
        ],
        default="none"
    )
    activity_json = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.order}. {self.title}"

    @property
    def youtube_id(self):
        if not self.youtube_url:
            return ""

        url = self.youtube_url.strip()

        m = re.search(r"youtu\.be/([A-Za-z0-9_-]{11})", url)
        if m:
            return m.group(1)

        m = re.search(r"[?&]v=([A-Za-z0-9_-]{11})", url)
        if m:
            return m.group(1)

        m = re.search(r"youtube\.com/embed/([A-Za-z0-9_-]{11})", url)
        if m:
            return m.group(1)

        return ""



