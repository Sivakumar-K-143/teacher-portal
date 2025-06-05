"""Models for the Teacher Portal app."""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Subject(models.Model):
    """Model representing a subject."""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.name)

class Student(models.Model):
    """Model representing a student."""
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.IntegerField()

    class Meta:
        unique_together = ('name', 'subject')  # Enforce uniqueness for (name, subject)

    def __str__(self):
        return f"{self.name} - {self.subject.name}"

class PasswordResetCode(models.Model):
    """Model for storing password reset codes."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        """Return True if more than 10 minutes old."""
        return self.created_at < timezone.now() - timedelta(minutes=10)
