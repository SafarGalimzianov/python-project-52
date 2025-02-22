from django.contrib import admin

# Register your models here.

from task_manager.tasks.models import Task

admin.site.register(Task)