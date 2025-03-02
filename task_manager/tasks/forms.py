from django import forms
from task_manager.tasks.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'name', 
            'status',
            'labels',
            'creator',
            'executor',
            'description'
        ]
        labels = {
            'name': 'Имя',
            'description': 'Описание',
            'status': 'Статус',
            'executor': 'Исполнитель', 
            'labels': 'Метки',
        }
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': ''}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['executor'].label_from_instance = lambda obj: str(obj)
