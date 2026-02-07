from django.db import models
from apps.accounts.models import ChildProfile
from apps.courses.models import Lesson

class LessonProgress(models.Model):
    child = models.ForeignKey(ChildProfile, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("child", "lesson")
