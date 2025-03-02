from django.views.generic.edit import FormMixin
from task_manager.users.models import User


class UserFormMixin(FormMixin):
    model = User
    content_extra = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context.update(self.context_extra)
        return context
