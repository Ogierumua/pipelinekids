from django.contrib import admin
from .models import ChildProfile, School, TeacherProfile, ClassRoom, StudentProfile

admin.site.register(ChildProfile)
admin.site.register(School)
admin.site.register(TeacherProfile)
admin.site.register(ClassRoom)
admin.site.register(StudentProfile)

# Register your models here.
