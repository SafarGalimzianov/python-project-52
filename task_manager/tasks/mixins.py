from django.views.generic.edit import FormMixin
from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskForm
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager.users.models import User

class TaskFormMixin(FormMixin):
    model = Task
    form_class = TaskForm
    context_extra = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['statuses'] = Status.objects.all()
        context['labels'] = Label.objects.all()
        context['executors'] = User.objects.all()
        if hasattr(self, 'filterset'):
            context['tasks'] = self.filterset.qs
        context['table_content'] = Task.objects.all()
        context.update(self.context_extra)
        return context
