"""Forms for the Teacher Portal app."""

from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    """Form for adding/editing students."""

    class Meta:
        model = Student
        fields = ['name', 'subject', 'marks']

    def clean_marks(self):
        """Ensure marks are between 0 and 100."""
        marks = self.cleaned_data['marks']
        if marks < 0 or marks > 100:
            raise forms.ValidationError("Marks must be between 0 and 100.")
        return marks
