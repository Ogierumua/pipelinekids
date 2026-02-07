from django.db import models

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()   # store HTML for MVP
    order = models.PositiveIntegerField()
    xp = models.PositiveIntegerField(default=10)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.order}. {self.title}"
