from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Count, Q, Sum

from .forms import ParentSignupForm, ChildProfileForm
from .models import ChildProfile, TeacherProfile, School, ClassRoom, StudentProfile

from apps.progress.models import LessonProgress
from apps.courses.models import Lesson


def signup(request):
    if request.method == "POST":
        form = ParentSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = ParentSignupForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def parent_dashboard(request):
    total_lessons = Lesson.objects.count()

    children = (
        ChildProfile.objects
        .filter(parent=request.user)
        .order_by("-created_at")
        .annotate(
            completed_lessons=Count(
                "lessonprogress",
                filter=Q(lessonprogress__completed=True)
            )
        )
    )

    return render(request, "dashboard/parent.html", {
        "children": children,
        "total_lessons": total_lessons,
    })


@login_required
def add_child(request):
    if request.method == "POST":
        form = ChildProfileForm(request.POST)
        if form.is_valid():
            child = form.save(commit=False)
            child.parent = request.user
            child.save()
            return redirect("parent_dashboard")
    else:
        form = ChildProfileForm()

    return render(request, "dashboard/child.html", {"form": form})


@login_required
def child_overview(request, child_id: int):
    child = get_object_or_404(ChildProfile, id=child_id, parent=request.user)

    total = Lesson.objects.count()
    completed = LessonProgress.objects.filter(child=child, completed=True).count()
    progress_pct = int((completed / total) * 100) if total else 0

    return render(request, "dashboard/child.html", {
        "child": child,
        "progress_pct": progress_pct,
        "completed": completed,
        "total": total,
    })


def _get_teacher_or_404(user):
    return get_object_or_404(TeacherProfile, user=user)


@login_required
def school_dashboard(request):
    """
    Teacher dashboard showing their school classes + stats.
    """
    teacher = _get_teacher_or_404(request.user)
    school = teacher.school

    classrooms = (
        ClassRoom.objects
        .filter(school=school)
        .annotate(student_count=Count("students"))
        .order_by("name")
    )

    # ✅ FIX: StudentProfile does NOT have school=... it has classroom=...
    totals = StudentProfile.objects.filter(classroom__school=school).aggregate(
        total_students=Count("id"),
        total_xp=Sum("xp"),
    )

    return render(request, "schools/dashboard.html", {
        "teacher": teacher,
        "school": school,
        "classrooms": classrooms,
        "total_students": totals.get("total_students") or 0,
        "totals": totals,
    })


@login_required
def school_create_class(request):
    teacher = _get_teacher_or_404(request.user)

    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        age_min = int(request.POST.get("age_min") or 8)
        age_max = int(request.POST.get("age_max") or 16)

        if name:
            ClassRoom.objects.create(
                school=teacher.school,
                teacher=teacher,
                name=name,
                age_min=age_min,
                age_max=age_max,
            )
    return redirect("school_dashboard")


@login_required
def class_detail(request, class_id: int):
    teacher = _get_teacher_or_404(request.user)
    classroom = get_object_or_404(ClassRoom, id=class_id, school=teacher.school)

    students = classroom.students.order_by("-xp", "name")

    return render(request, "schools/class_detail.html", {
        "teacher": teacher,
        "school": teacher.school,
        "classroom": classroom,
        "students": students,
    })


@login_required
def class_add_student(request, class_id: int):
    teacher = _get_teacher_or_404(request.user)
    classroom = get_object_or_404(ClassRoom, id=class_id, school=teacher.school)

    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        age = int(request.POST.get("age") or 10)

        if name:
            StudentProfile.objects.create(
                classroom=classroom,
                name=name,
                age=age,
            )

    return redirect("class_detail", class_id=classroom.id)


@login_required
def after_login(request):
    """
    Single redirect point after login.
    - Teachers -> school dashboard
    - Parents  -> parent dashboard
    """
    if TeacherProfile.objects.filter(user=request.user).exists():
        return redirect("school_dashboard")

    return redirect("parent_dashboard")


@login_required
def school_lessons(request, class_id: int):
    teacher = _get_teacher_or_404(request.user)
    classroom = get_object_or_404(ClassRoom, id=class_id, school=teacher.school)

    lessons = Lesson.objects.order_by("order")
    students = classroom.students.order_by("name")

    return render(request, "schools/lessons.html", {
        "teacher": teacher,
        "school": teacher.school,
        "classroom": classroom,
        "lessons": lessons,
        "students": students,
    })


@login_required
def school_lesson_detail(request, class_id: int, lesson_id: int):
    teacher = _get_teacher_or_404(request.user)
    classroom = get_object_or_404(ClassRoom, id=class_id, school=teacher.school)
    lesson = get_object_or_404(Lesson, id=lesson_id)

    students = classroom.students.order_by("name")

    return render(request, "schools/lesson_detail.html", {
        "teacher": teacher,
        "school": teacher.school,
        "classroom": classroom,
        "lesson": lesson,
        "students": students,
    })


@login_required
def school_complete_lesson(request, class_id: int, lesson_id: int, student_id: int):
    teacher = _get_teacher_or_404(request.user)
    classroom = get_object_or_404(ClassRoom, id=class_id, school=teacher.school)
    lesson = get_object_or_404(Lesson, id=lesson_id)
    student = get_object_or_404(StudentProfile, id=student_id, classroom=classroom)

    # ✅ Add XP when teacher marks complete
    student.xp += int(getattr(lesson, "xp", 10))
    student.save(update_fields=["xp"])

    messages.success(request, f"✅ {student.name} completed '{lesson.title}' (+{lesson.xp} XP).")

    return redirect("school_lesson_detail", class_id=classroom.id, lesson_id=lesson.id)
