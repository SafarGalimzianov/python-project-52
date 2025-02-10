from django import forms
from task_manager.models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status', 'labels', 'responsible', 'description']