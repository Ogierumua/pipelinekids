from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from apps.accounts.models import ChildProfile
from apps.progress.models import LessonProgress
from .models import Lesson
from apps.billing.utils import subscription_required  # we'll define below

@login_required
@subscription_required
def lesson_list(request, child_id: int):
    child = get_object_or_404(ChildProfile, id=child_id, parent=request.user)
    lessons = Lesson.objects.all()
    completed_ids = set(LessonProgress.objects.filter(child=child, completed=True).values_list("lesson_id", flat=True))
    return render(request, "lessons/list.html", {"child": child, "lessons": lessons, "completed_ids": completed_ids})

@login_required
@subscription_required
def lesson_detail(request, child_id: int, lesson_id: int):
    child = get_object_or_404(ChildProfile, id=child_id, parent=request.user)
    lesson = get_object_or_404(Lesson, id=lesson_id)

    if request.method == "POST":
        prog, _ = LessonProgress.objects.get_or_create(child=child, lesson=lesson)
        if not prog.completed:
            prog.completed = True
            prog.save()
        return redirect("lesson_list", child_id=child.id)

    completed = LessonProgress.objects.filter(child=child, lesson=lesson, completed=True).exists()
    return render(request, "lessons/detail.html", {"child": child, "lesson": lesson, "completed": completed})

