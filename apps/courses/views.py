from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST

from apps.accounts.models import ChildProfile
from apps.progress.models import LessonProgress
from .models import Lesson


@login_required
def lesson_list(request, child_id: int):
    child = get_object_or_404(ChildProfile, id=child_id, parent=request.user)
    lessons = Lesson.objects.all().order_by("order")

    completed_ids = set(
        LessonProgress.objects.filter(
            child=child, completed=True
        ).values_list("lesson_id", flat=True)
    )

    return render(request, "lessons/list.html", {
        "child": child,
        "lessons": lessons,
        "completed_ids": completed_ids,
    })


@login_required
def lesson_detail(request, child_id: int, lesson_id: int):
    child = get_object_or_404(ChildProfile, id=child_id, parent=request.user)
    lesson = get_object_or_404(Lesson, id=lesson_id)

    completed = LessonProgress.objects.filter(
        child=child, lesson=lesson, completed=True
    ).exists()

    return render(request, "lessons/detail.html", {
        "child": child,
        "lesson": lesson,
        "completed": completed,
    })


@login_required
@require_POST
def lesson_complete(request, child_id: int, lesson_id: int):
    child = get_object_or_404(ChildProfile, id=child_id, parent=request.user)
    lesson = get_object_or_404(Lesson, id=lesson_id)

    prog, created = LessonProgress.objects.get_or_create(
        child=child,
        lesson=lesson,
        defaults={
            "completed": True,
            "completed_at": timezone.now()
        }
    )

    xp_awarded = 0

    if created:
        child.xp += int(lesson.xp or 0)
        child.save(update_fields=["xp"])
        xp_awarded = int(lesson.xp or 0)

    next_lesson = Lesson.objects.filter(
        order__gt=lesson.order
    ).order_by("order").first()

    next_url = f"/lessons/{child.id}/{next_lesson.id}/" if next_lesson else None

    return JsonResponse({
        "ok": True,
        "xp_awarded": xp_awarded,
        "child_xp": child.xp,
        "next_url": next_url,
    })
