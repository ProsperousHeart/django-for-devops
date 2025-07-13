from django import forms
from .models import DailyNote


class DailyNoteForm(forms.ModelForm):

    class Meta:
        model = DailyNote
        fields = ["title"]
