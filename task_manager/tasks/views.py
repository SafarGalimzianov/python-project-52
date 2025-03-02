from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import \
    UpdateView, DeleteView, CreateView, DetailView
from django.urls import reverse_lazy
from django_filters.views import FilterView
from task_manager.tasks.models import Task
from task_manager.tasks.mixins import TaskFormMixin
from task_manager.tasks.filters import TaskFilter
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager.users.models import User
from task_manager.common.messages import TASK_MESSAGES
import logging

logger = logging.getLogger(__name__)

class TaskPageView(LoginRequiredMixin, FilterView, TaskFormMixin):
    template_name = 'tasks/index_tasks.html'
    filterset_class = TaskFilter
    context_extra = {
        'title': 'Tasks',
        'table_headers': [
            'ID',
            'Name',
            'Status',
            'Labels',
            'Creator', 
            'Executors',
            'Description',
            'Actions'
        ],
        'form_action': 'task_create',
        'button_create': 'Создать задачу',
        'statuses': Status.objects.all(),
        'labels': Label.objects.all(),
        'executors': User.objects.all(),
    }

    def get(self, request, *args, **kwargs):
        logger.info(f"\nGET params: {request.GET}")
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        filterset = self.filterset_class(
            self.request.GET,
            queryset=queryset,
            request=self.request,
        )
        filtered_qs = filterset.qs
        logger.info(f'Applied filters - \
                    status: {self.request.GET.get("status")}, \
                    labels: {self.request.GET.get("labels")}, \
                    count: {filtered_qs.count()}'
        )
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
    template_name = 'create.html'
    success_url = reverse_lazy('tasks')
    context_extra = {
        'title': 'Tasks',
        'table_headers': [
            'ID',
            'Status',
            'Labels',
            'Creator', 
            'Executors',
            'Description',
            'Actions'
        ],
        'form_action': 'task_create',
        'button': 'Создать',
        'statuses': Status.objects.all(),
        'labels': Label.objects.all(),
        'executors': User.objects.all(),
    }
    messages_show = {
        'error': TASK_MESSAGES['create_error'],
        'success': TASK_MESSAGES['create'],
    }
    
    def form_valid(self, form):
        form.instance.creator = self.request.user
        logger.info(f'Creating task when logged in as {self.request.user}')
        messages.success(self.request, self.messages_show['success'], extra_tags='.alert')
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    self.request,
                    f'{self.messages_show["error"]}: {field}: {error}',
                    extra_tags='.alert',
                )
        return redirect('task_create')

class TaskUpdatePageView(LoginRequiredMixin, TaskFormMixin, UpdateView):
    template_name = 'update.html'
    success_url = reverse_lazy('tasks')
    messages_show = {
        'success': TASK_MESSAGES['update'],
    }

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        self.original_description = obj.description
        return obj

    def form_valid(self, form):
        messages.success(self.request, self.messages_show['success'], extra_tags='.alert')
        return super().form_valid(form)

class TaskDeletePageView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks')
    template_name = 'delete.html'
    context_extra = {
        'header': 'Tasks',
        'fields_names': ['ID', 'name'],
    }
    messages_show = {
        'error': TASK_MESSAGES['delete_error'],
        'success': TASK_MESSAGES['delete'],
    }

    def get(self, request, *args, **kwargs):
        object_to_delete = self.get_object()
        if object_to_delete.creator.id != request.user.id:
            logger.info(f'{request.user} CANNOT delete task \
                        created by {object_to_delete.creator}')
            messages.error(
                self.request,
                self.messages_show['error'],
                extra_tags='.alert'
            )
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        object_to_delete = self.get_object()
        if object_to_delete.creator.id != request.user.id:
            logger.info(f"{request.user} CANNOT delete task \
                        created by {object_to_delete.creator}")
            messages.error(
                self.request,
                self.messages_show['error'],
                extra_tags='.alert'
            )
            return redirect(self.success_url)
        
        response = super().post(request, *args, **kwargs)
        messages.success(
            self.request,
            self.messages_show['success'],
            extra_tags='.alert',
        )
        return response
        
    def dispatch(self, request, *args, **kwargs):
        logger.info(f"{request.user} now in \
                    TaskDeletePageView dispatch method")
        return super(DeleteView, self).dispatch(request, *args, **kwargs)
