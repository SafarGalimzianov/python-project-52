from django import forms
from task_manager.tasks.models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'status', 'labels', 'creator', 'executor', 'description']

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['executor'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"