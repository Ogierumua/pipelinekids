from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .forms import ParentSignupForm, ChildProfileForm
from .models import ChildProfile
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
    children = ChildProfile.objects.filter(parent=request.user).order_by("-created_at")
    return render(request, "dashboard/parent.html", {"children": children})

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
        "total": total
    })
