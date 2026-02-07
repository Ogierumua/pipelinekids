from django.urls import path
from . import views

urlpatterns = [
    path("<int:child_id>/", views.lesson_list, name="lesson_list"),
    path("<int:child_id>/<int:lesson_id>/", views.lesson_detail, name="lesson_detail"),
]
