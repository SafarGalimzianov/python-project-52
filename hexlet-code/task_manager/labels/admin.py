from django.contrib import admin

# Register your models here.
from task_manager.labels.models import Label

admin.site.register(Label)