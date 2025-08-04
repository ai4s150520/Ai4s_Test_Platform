# In core/forms.py

from django import forms
from django.forms import inlineformset_factory
from .models import Test, Question, Answer

class TestCreateForm(forms.ModelForm):
    """
    A form for creating a new Test. This will be used in the 'add_test.html' template.
    """
    class Meta:
        model = Test
        # Specify the fields you want the user to fill out
        fields = ['title', 'category', 'description', 'difficulty', 'duration_in_minutes', 'image']
        
        # Add Bootstrap classes and placeholders to the form widgets for styling
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., SAP FICO Fundamentals'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter a detailed description of the test...'}),
            'difficulty': forms.Select(attrs={'class': 'form-select'}),
            'duration_in_minutes': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 60'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'duration_in_minutes': 'Duration (in minutes)',
        }

class QuestionForm(forms.ModelForm):
    """A form for a single Question."""
    class Meta:
        model = Question
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control question-text', 'rows': 3, 'placeholder': 'Enter the full text for the question'}),
        }

# An InlineFormSet is a powerful Django tool that lets you manage related objects
# (like multiple Answers for one Question) on the same page.
AnswerFormSet = inlineformset_factory(
    Question,  # The parent model
    Answer,    # The child model being edited
    fields=('text', 'is_correct'),
    extra=4,   # Start by showing 4 empty answer forms
    can_delete=True, # Allow deleting answers
    widgets={
        'text': forms.TextInput(attrs={'class': 'form-control answer-text mb-2', 'placeholder': 'Enter answer option'}),
        'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input is-correct-checkbox'}),
    }
)