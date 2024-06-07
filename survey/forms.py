from django import forms
from django.contrib.auth.forms import UserCreationForm
#from .models import User, StudentProfile, TeacherProfile
from .models import Question, Uenseignement

from .models import Course


class UenseignementForm(forms.ModelForm):
    class Meta:
        model = Uenseignement
        fields = ['name']
        widgets = {
        }
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'date_debut', 'date_fin', 'total_marks', 'uenseignement']
        widgets = {
            'date_fin': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_debut': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}),
        }



class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['course', 'text', 'options', 'response', 'marks']
        widgets = {
            'course': forms.Select(attrs={'class': 'input'}),
            'text': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Entrez la question'}),
            'response': forms.Select(attrs={'class': 'input'}),
           # 'options': forms.TextInput(attrs={'class': 'input'}),
            'marks': forms.NumberInput(attrs={'class': 'input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['options'].widget = forms.HiddenInput()
        self.fields['response'].widget = forms.Select(choices=[('', '---')])  # Initialiser avec un choix vide

    def set_options_choices(self, options_list):
        self.fields['response'].widget.choices = [(option, option) for option in options_list]


