from django.db import models
import re

class Lesson(models.Model):
    # ✅ NEW: Modules (to avoid long list of missions)
    MODULE_CHOICES = [
        ("computer_basics", "Computer Basics"),
        ("systems_logic", "Systems Logic & Critical Thinking"),
        ("careers", "Careers"),
        ("logic5", "5-in-1: Logic Mission"),

    ]

    module = models.CharField(
        max_length=40,
        choices=MODULE_CHOICES,
        default="computer_basics"
    )

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
            ("mouse", "Mouse Practice"),
            ("typing", "Keyboard Game"),
            ("tidy", "Tidy the Computer"),
            ("triple", "3-in-1 Digital Skills"),
            ("foundations3", "3-in-1: Digital Foundations"),
            ("files3", "3-in-1: Files & Folders"),
            ("word5", "5-in-1: Microsoft Word"),
            ("excel8", "8-in-1: Excel Basics"),
            ("ppt10", "10-in-1: Microsoft PowerPoint Playground"),
            ("cp12", "12-in-1: Control Panel Playground"),
            ("safety12", "12-in-1: Safety + Good/Not Good"),
            ("jobs8", "8-in-1: Jobs That Use Computers"),
            ("logic5", "5-in-1: Logic & Critical Thinking"),
            ("logic5", "5-in-1: IPO + Decisions + Loops + Data"),
            ("sys5", "5-in-1: Systems + Memory + Storage"),
            ("net5", "5-in-1: Internet + Apps + Networks"),
            ("teams8", "8-in-1: Speed + Safety + Tech Teams"),
            ("career8", "8-in-1: Engineers + Data Engineers"),
            ("netcloud8", "8-in-1: Network + Cloud Engineers"),
            ("cyberai8", "8-in-1: Cybersecurity + AI Engineers"),
            ("teamtools8", "8-in-1: Teams + Tools Playground"),
            ("project8", "8-in-1: Projects + Ethics + Paths"),



            
            






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
