from django.views.generic.edit import FormMixin
from task_manager.statuses.models import Status
from task_manager.statuses.forms import StatusForm


class StatusFormMixin(FormMixin):
    model = Status
    form_class = StatusForm
    context_extra = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context.update(self.context_extra)
        return context
