from django import forms
from task_manager.models import Task
from task_manager.users.models import User
from task_manager.labels.models import Label
from task_manager.statuses.models import Status

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status', 'labels', 'responsible', 'description']

class SearchForm(forms.Form):
    ...