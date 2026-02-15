import re
from urllib.parse import urlencode
from django.conf import settings
from django.db import models

YOUTUBE_ID_RE = re.compile(r"(?:v=|youtu\.be/|embed/)([A-Za-z0-9_-]{11})")

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    youtube_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField()
    xp = models.PositiveIntegerField(default=10)

    # ... your fields ...

    @property
    def youtube_id(self):
        if not self.youtube_url:
            return None
        m = YOUTUBE_ID_RE.search(self.youtube_url)
        return m.group(1) if m else None

    @property
    def youtube_watch_url(self):
        if not self.youtube_id:
            return ""
        return f"https://www.youtube.com/watch?v={self.youtube_id}"

    @property
    def youtube_thumbnail(self):
        if not self.youtube_id:
            return ""
        return f"https://img.youtube.com/vi/{self.youtube_id}/hqdefault.jpg"

    @property
    def youtube_embed_url(self):
        """
        Important:
        - Use nocookie domain (better for schools).
        - Only add origin if SITE_URL is a real https domain (not localhost).
        """
        if not self.youtube_id:
            return ""

        params = {
            "rel": 0,
            "modestbranding": 1,
            "playsinline": 1,
        }

        site_url = getattr(settings, "SITE_URL", "")
        if site_url and site_url.startswith("https://") and "onrender.com" in site_url:
            params["origin"] = site_url

        return f"https://www.youtube-nocookie.com/embed/{self.youtube_id}?{urlencode(params)}"
