from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from apps.accounts.models import ChildProfile
from apps.courses.models import Lesson
from apps.progress.models import LessonProgress
from .models import Certificate
from .utils import make_certificate_id, build_certificate_pdf

@login_required
def download_certificate(request, child_id: int):
    child = get_object_or_404(ChildProfile, id=child_id, parent=request.user)

    total = Lesson.objects.count()
    completed = LessonProgress.objects.filter(child=child, completed=True).count()
    if total == 0 or completed < total:
        return HttpResponse("Complete all lessons to unlock certificate.", status=403)

    cert = Certificate.objects.filter(child=child).first()
    if not cert:
        cert = Certificate.objects.create(child=child, certificate_id=make_certificate_id())

    pdf_bytes = build_certificate_pdf(child.name, cert.certificate_id)
    resp = HttpResponse(pdf_bytes, content_type="application/pdf")
    resp["Content-Disposition"] = f'attachment; filename="PipelineKids-Certificate-{child.name}.pdf"'
    return resp
