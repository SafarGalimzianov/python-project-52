from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskForm

class TaskFormMixin(FormMixin):
    model = Task
    form_class = TaskForm
    context_extra = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context.update(self.context_extra)
        return context

class TaskPageView(LoginRequiredMixin, TaskFormMixin, ListView):
    template_name = 'index_tasks.html'
    context_object_name = 'table_content'
    context_extra = {
        'title': 'Tasks',
        'table_headers': ['ID', 'Status', 'Labels', 'Creator', 
                         'Responsible', 'Description', 'Actions'],
        'form_action': 'task_create',
    }

class TaskCreatePageView(LoginRequiredMixin, TaskFormMixin, CreateView):
    template_name = 'create.html'
    success_url = reverse_lazy('tasks')

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Error in {field}: {error}")
        return redirect('tasks')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        if not self.request.user.is_staff:
            form.instance.responsible = self.request.user
        messages.success(self.request, 'Task created successfully')
        return super().form_valid(form)

class TaskUpdatePageView(LoginRequiredMixin, TaskFormMixin, UpdateView):
    template_name = 'update.html'
    success_url = reverse_lazy('tasks')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        self.original_description = obj.description
        return obj

    def form_valid(self, form):
        messages.success(
            self.request,
            f'{self.original_description} updated to {form.instance.description} successfully'
        )
        return super().form_valid(form)

class TaskDeletePageView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks')
    
    def get(self, request, *args, **kwargs):
        """Override get to handle deletion without template"""
        return self.delete(request, *args, **kwargs)
