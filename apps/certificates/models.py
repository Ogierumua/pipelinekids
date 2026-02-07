from django.db import models
from apps.accounts.models import ChildProfile

class Certificate(models.Model):
    child = models.ForeignKey(ChildProfile, on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)
    certificate_id = models.CharField(max_length=20, unique=True)
