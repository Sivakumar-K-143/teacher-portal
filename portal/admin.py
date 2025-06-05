"""Admin registration for Teacher Portal."""

from django.contrib import admin
from .models import Student, Subject, PasswordResetCode

admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(PasswordResetCode)
