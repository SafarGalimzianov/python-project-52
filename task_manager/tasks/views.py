from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import UpdateView, DeleteView, CreateView, DetailView
from django.urls import reverse_lazy
from django_filters.views import FilterView
from task_manager.tasks.models import Task
from task_manager.tasks.mixins import TaskFormMixin
from task_manager.tasks.filters import TaskFilter
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager.users.models import User
import logging

logger = logging.getLogger(__name__)

class TaskPageView(LoginRequiredMixin, FilterView, TaskFormMixin):
    template_name = 'tasks/test.html'
    filterset_class = TaskFilter
    context_extra = {
        'title': 'Tasks',
        'table_headers': ['ID', 'Name', 'Status', 'Labels', 'Creator', 
                         'Executors', 'Description', 'Actions'],
        'form_action': 'task_create',
        'statuses': Status.objects.all(),
        'labels': Label.objects.all(),
        'executors': User.objects.all(),
    }

    def get(self, request, *args, **kwargs):
        logger.info(f"\nGET params: {request.GET}")
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        filterset = self.filterset_class(self.request.GET, queryset=queryset, request=self.request)
        filtered_qs = filterset.qs
        logger.info(f"Applied filters - status: {self.request.GET.get('status')}, labels: {self.request.GET.get('labels')}, count: {filtered_qs.count()}")
        return filtered_qs


class TaskShowPageView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/show_task.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Task Details'
        return context

class TaskCreatePageView(LoginRequiredMixin, TaskFormMixin, CreateView):
    template_name = 'tasks/create_tasks.html'
    success_url = reverse_lazy('tasks')
    context_extra = {
        'title': 'Tasks',
        'table_headers': ['ID', 'Status', 'Labels', 'Creator', 
                         'Executors', 'Description', 'Actions'],
        'form_action': 'task_create',
        'button': 'Создать',
        'statuses': Status.objects.all(),
        'labels': Label.objects.all(),
        'executors': User.objects.all(),
    }

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Error in {field}: {error}")
        return redirect('task_create')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        '''
        if not self.request.user.is_staff:
            form.instance.responsible = self.request.user
        '''
        logger.info(f'[TASKCREATEPAGEVIEW FORM_VALID] Creating task when logged in as {self.request.user}')
        messages.success(self.request, 'Задача успешно создана')
        return super().form_valid(form)

class TaskUpdatePageView(LoginRequiredMixin, TaskFormMixin, UpdateView):
    template_name = 'update.html'
    success_url = reverse_lazy('tasks')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        self.original_description = obj.description
        return obj

    def form_valid(self, form):
        messages.success(self.request, 'Задача успешно изменена')
        '''
        messages.success(
            self.request,
            f'{self.original_description} updated to {form.instance.description} successfully'
        )
        '''
        return super().form_valid(form)

class TaskDeletePageView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks')

    template_name = 'delete.html'
    context_extra = {
        'header': 'Statuses',
        'fields_names': ['ID', 'name'],
    }

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, 'Задача успешно удалена', extra_tags='.alert')
        return super().dispatch(request, *args, **kwargs)

    '''
    def get(self, request, *args, **kwargs):
        """Override get to handle deletion without template"""
        return self.delete(request, *args, **kwargs)
    '''