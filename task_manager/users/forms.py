from django.contrib.auth.forms import UserChangeForm
from task_manager.users.models import User

class UserUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['username']