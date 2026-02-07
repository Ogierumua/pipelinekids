from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("dashboard/", views.parent_dashboard, name="parent_dashboard"),
    path("children/add/", views.add_child, name="add_child"),
    path("children/<int:child_id>/", views.child_overview, name="child_overview"),
]