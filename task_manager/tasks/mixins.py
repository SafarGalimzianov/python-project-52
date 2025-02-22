from django.views.generic.edit import FormMixin
from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskForm

class TaskFormMixin(FormMixin):
    model = Task
    form_class = TaskForm
    context_extra = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        try:
            context['tasks'] = self.filterset.qs
            context['table_content'] = Task.objects.all()
        except AttributeError:
            pass
        context.update(self.context_extra)
        return context
