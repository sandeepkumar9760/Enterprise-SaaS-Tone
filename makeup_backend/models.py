# Create your models here.
from django.db import models
import uuid


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


class MakeUpClass(models.Model):
    subject = models.CharField(max_length=200)
    classroom = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField(blank=True)
    remedial_code = models.CharField(max_length=12, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.remedial_code:
            self.remedial_code = str(uuid.uuid4()).replace("-", "")[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.subject} - {self.date}"


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    makeup_class = models.ForeignKey(MakeUpClass, on_delete=models.CASCADE)
    marked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'makeup_class')