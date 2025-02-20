from django.conf import settings
from django.db import models
from task_manager.statuses.models import Status
from task_manager.labels.models import Label

class Task(models.Model):
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name='tasks')
    labels = models.ManyToManyField(Label, related_name='tasks')
    creator = models.ForeignKey(
        'auth.User',  # Updated reference
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_tasks'
    )
    responsible = models.ForeignKey(
        'auth.User',  # Updated reference
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='responsible_tasks'
    )
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.description