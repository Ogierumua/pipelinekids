from django.urls import path
from . import views

urlpatterns = [
    path("<int:child_id>/download/", views.download_certificate, name="download_certificate"),
]

