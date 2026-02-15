from django.urls import path
from . import views

urlpatterns = [
    # ✅ Modules home
    path("<int:child_id>/", views.modules_home, name="modules_home"),

    # ✅ Lessons for a module
    path("<int:child_id>/module/<str:module_key>/", views.lesson_list, name="lesson_list"),

    # ✅ Lesson detail inside module
    path("<int:child_id>/module/<str:module_key>/<int:lesson_id>/", views.lesson_detail, name="lesson_detail"),

    # ✅ Complete lesson inside module
    path("<int:child_id>/module/<str:module_key>/<int:lesson_id>/complete/", views.lesson_complete, name="lesson_complete"),
]

