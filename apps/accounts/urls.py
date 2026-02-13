from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("dashboard/", views.parent_dashboard, name="parent_dashboard"),
    path("children/add/", views.add_child, name="add_child"),
    path("children/<int:child_id>/", views.child_overview, name="child_overview"),
    # Schools (Teacher)
    path("schools/dashboard/", views.school_dashboard, name="school_dashboard"),
    path("schools/classes/create/", views.school_create_class, name="school_create_class"),
    path("schools/classes/<int:class_id>/", views.class_detail, name="class_detail"),
    path("schools/classes/<int:class_id>/students/add/", views.class_add_student, name="class_add_student"),
    path("after-login/", views.after_login, name="after_login"),
    path("schools/classes/<int:class_id>/lessons/", views.school_lessons, name="school_lessons"),
    path("schools/classes/<int:class_id>/lessons/<int:lesson_id>/", views.school_lesson_detail, name="school_lesson_detail"),
    path("schools/classes/<int:class_id>/lessons/<int:lesson_id>/student/<int:student_id>/complete/", views.school_complete_lesson, name="school_complete_lesson"),

    

]