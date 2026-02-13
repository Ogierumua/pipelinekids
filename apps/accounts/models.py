from django.db import models
from django.contrib.auth.models import User

class ChildProfile(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="children")
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    xp = models.PositiveIntegerField(default=0)  # ✅ ADD THIS

    def __str__(self):
        return f"{self.name} ({self.age})"
    
    
class School(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=50, default="Nigeria")  # Nigeria / UK
    city = models.CharField(max_length=120, blank=True)
    contact_email = models.EmailField(blank=True)

    # Optional: licensing/status for MVP sales
    status = models.CharField(max_length=30, default="trial")  # trial / active / inactive
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.country})"


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="teacher_profile")
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="teachers")
    title = models.CharField(max_length=50, blank=True)  # Mr/Mrs/Coach etc

    def __str__(self):
        return f"{self.user.username} - {self.school.name}"


class ClassRoom(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="classes")
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name="classes")
    name = models.CharField(max_length=120)   # e.g. "Primary 5A" / "Year 6"
    age_min = models.PositiveIntegerField(default=8)
    age_max = models.PositiveIntegerField(default=16)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.school.name} - {self.name}"


class StudentProfile(models.Model):
    """
    MVP: Students do NOT need user accounts.
    Teacher records progress + XP for the student.
    Later: add User OneToOne if you want student logins.
    """
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name="students")
    name = models.CharField(max_length=120)
    age = models.PositiveIntegerField()
    xp = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.classroom.name})"
