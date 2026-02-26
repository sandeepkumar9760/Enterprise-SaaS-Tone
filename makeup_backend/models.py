# Create your models here.
from django.db import models
import uuid
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('FACULTY', 'Faculty'),
        ('STUDENT', 'Student'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
class Faculty(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=150)
    roll_number = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.roll_number


import uuid
from django.db import models


from django.db import models
from django.utils import timezone
from datetime import datetime
import uuid


class MakeUpClass(models.Model):
    subject = models.CharField(max_length=100)
    classroom = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    remedial_code = models.CharField(max_length=20, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.remedial_code:
            self.remedial_code = self.generate_code()
        super().save(*args, **kwargs)

    def generate_code(self):
        return "RC-" + uuid.uuid4().hex[:6].upper()

    @property
    def status(self):
        class_datetime = datetime.combine(self.date, self.time)

        # Make timezone-aware comparison
        class_datetime = timezone.make_aware(class_datetime)

        if class_datetime < timezone.now():
            return "Expired"
        return "Active"

    def __str__(self):
        return f"{self.subject} - {self.remedial_code}"


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    makeup_class = models.ForeignKey(MakeUpClass, on_delete=models.CASCADE)
    marked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'makeup_class')