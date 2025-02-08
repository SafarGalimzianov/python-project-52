from django.contrib import admin

# Register your models here.
from task_manager.statuses.models import Status

admin.site.register(Status)