from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST

from apps.accounts.models import ChildProfile
from apps.progress.models import LessonProgress
from .models import Lesson


# ✅ Your 3 modules (must match Lesson.MODULE_CHOICES keys)
MODULES = [
    ("computer_basics", "Computer Basics", "10 Missions", "Start here: mouse, keyboard, files, Word, Excel, PowerPoint."),
    ("systems_logic", "Systems Logic & Critical Thinking", "5 Missions", "Think like an engineer: steps, patterns, decisions, debugging."),
    ("careers", "Careers", "5 Missions", "Explore jobs and tools: data, network, cloud, cyber, AI."),
]


def _get_child(request, child_id: int):
    return get_object_or_404(ChildProfile, id=child_id, parent=request.user)


@login_required
def modules_home(request, child_id: int):
    """
    ✅ Modules landing page (3 cards). Kids pick ONE module at a time.
    """
    child = _get_child(request, child_id)

    # Stats per module (how many lessons + how many completed)
    completed_ids = set(
        LessonProgress.objects.filter(child=child, completed=True)
        .values_list("lesson_id", flat=True)
    )

    module_cards = []
    for key, title, count_label, desc in MODULES:
        lessons_in_module = list(Lesson.objects.filter(module=key).order_by("order"))
        total = len(lessons_in_module)
        done = sum(1 for l in lessons_in_module if l.id in completed_ids)
        pct = int((done / total) * 100) if total else 0

        module_cards.append({
            "key": key,
            "title": title,
            "count_label": count_label,
            "desc": desc,
            "total": total,
            "done": done,
            "pct": pct,
        })

    return render(request, "lessons/modules.html", {
        "child": child,
        "modules": module_cards,
    })


@login_required
def lesson_list(request, child_id: int, module_key: str):
    """
    ✅ Lesson list for ONE module (no long list anymore).
    """
    child = _get_child(request, child_id)

    # Validate module
    valid_keys = {m[0] for m in MODULES}
    if module_key not in valid_keys:
        # simple 404 behaviour
        raise Exception("Invalid module key")

    lessons = Lesson.objects.filter(module=module_key).order_by("order")

    completed_ids = set(
        LessonProgress.objects.filter(child=child, completed=True)
        .values_list("lesson_id", flat=True)
    )

    # For heading
    module_title = next((m[1] for m in MODULES if m[0] == module_key), module_key)

    return render(request, "lessons/list.html", {
        "child": child,
        "lessons": lessons,
        "completed_ids": completed_ids,
        "module_key": module_key,
        "module_title": module_title,
    })


@login_required
def lesson_detail(request, child_id: int, module_key: str, lesson_id: int):
    """
    Lesson details inside a module.
    """
    child = _get_child(request, child_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, module=module_key)

    completed = LessonProgress.objects.filter(child=child, lesson=lesson, completed=True).exists()

    module_title = next((m[1] for m in MODULES if m[0] == module_key), module_key)

    return render(request, "lessons/detail.html", {
        "child": child,
        "lesson": lesson,
        "completed": completed,
        "module_key": module_key,
        "module_title": module_title,
    })


@login_required
@require_POST
def lesson_complete(request, child_id: int, module_key: str, lesson_id: int):
    """
    Mark lesson complete, award XP once, and return next lesson INSIDE SAME MODULE.
    """
    child = _get_child(request, child_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, module=module_key)

    prog, created = LessonProgress.objects.get_or_create(
        child=child,
        lesson=lesson,
        defaults={"completed": True, "completed_at": timezone.now()},
    )

    xp_awarded = 0
    if created:
        child.xp += int(lesson.xp or 0)
        child.save(update_fields=["xp"])
        xp_awarded = int(lesson.xp or 0)

    # ✅ next lesson in SAME module
    next_lesson = (
        Lesson.objects.filter(module=module_key, order__gt=lesson.order)
        .order_by("order")
        .first()
    )

    next_url = f"/lessons/{child.id}/module/{module_key}/{next_lesson.id}/" if next_lesson else None

    return JsonResponse({
        "ok": True,
        "xp_awarded": xp_awarded,
        "child_xp": child.xp,
        "next_url": next_url,
    })
