from django.contrib import admin

# Register your models here.
from task_manager.users.models import User

admin.site.register(User)