from django.db import models
from django.contrib.auth.models import User

class Subscription(models.Model):
    parent = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=255, blank=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=50, default="inactive")


# Create your models here.
