from django import forms
from django.forms import ModelForm

from .models import Task

class CreateNewTask(forms.Form):
    title = forms.CharField(
        label="Title", max_length=200,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder':'Write a title'}
        )
    )
    description = forms.CharField(
        label="Description", widget=forms.Textarea(
            attrs={
                'class': 'form-control', 'placeholder':'Write a description'
            }
        )
    )
    important = forms.BooleanField(
        label="Important", widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

class CreateNewProject(forms.Form):
    name = forms.CharField(label="Nombre del proyecto", max_length=200, widget=forms.TextInput(attrs={'class': 'input'}))

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder':'Write a title'}
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Write a description'
                }
            ),
            'important': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            )
        }