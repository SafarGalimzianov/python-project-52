from django.views.generic.edit import FormMixin
from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label

class LabelFormMixin(FormMixin):
    model = Label
    form_class = LabelForm
    context_extra = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context.update(self.context_extra)
        return context
