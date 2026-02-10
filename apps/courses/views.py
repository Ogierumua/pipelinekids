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
    

    completed = LessonProgress.objects.filter(child=child, lesson=lesson,  completed=True).exists()

    return render(
        request,
        "lessons/detail.html",
        {"child": child, "lesson": lesson, "completed": completed},
    )

from django.http import JsonResponse
from django.views.decorators.http import require_POST

def _add_xp_to_child(child, amount: int):
    """
    We don’t know your exact field name on ChildProfile,
    so this safely supports common options.
    """
    for field in ("xp", "total_xp", "xp_total"):
        if hasattr(child, field):
            setattr(child, field, (getattr(child, field) or 0) + amount)
            child.save(update_fields=[field])
            return True
    return False  # if no xp field exists

@login_required
@subscription_required
@require_POST
def lesson_complete(request, child_id: int, lesson_id: int):
    child = get_object_or_404(ChildProfile, id=child_id, parent=request.user)
    lesson = get_object_or_404(Lesson, id=lesson_id)

    prog, _ = LessonProgress.objects.get_or_create(child=child, lesson=lesson)

    # ✅ Award only once
    if not prog.completed:
        prog.completed = True
        prog.save(update_fields=["completed"])

        # ✅ XP from lesson.xp
        _add_xp_to_child(child, int(lesson.xp or 0))

    # ✅ Find next lesson by order
    # ✅ Find next lesson by order
    next_lesson = Lesson.objects.filter(order__gt=lesson.order).order_by("order").first()
    next_url = None
    if next_lesson:
        next_url = f"/lessons/{child.id}/{next_lesson.id}/"
        
    # ✅ Optional badge from activity_json
    badge = None
    if lesson.activity_json and isinstance(lesson.activity_json, dict):
        badge = lesson.activity_json.get("badge")


    return JsonResponse({
        "ok": True,
        "completed": True,
        "xp_awarded": int(lesson.xp or 0),
        "badge": badge,
        "next_url": next_url,
    })
    
    




