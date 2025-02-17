from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from task_manager.models import Task
from task_manager.users.models import User
from task_manager.forms import TaskForm
from task_manager.filters import TaskFilter
from django_filters.views import FilterView


class HomePageView(FilterView):
    model = Task
    filterset_class = TaskFilter
    template_name = 'home.html'
    context_object_name = 'tasks'

    ...

"""
class TaskModifyMixin:
    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if task.creator != request.user:
            messages.error(request, f'Only the creator can {self.action} the task')
            return redirect('tasks')
        return super().dispatch(request, *args, **kwargs)
"""
"""
class TaskFormMixin(FormMixin):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_staff:
            form.fields['responsible'].disabled = True
            form.initial['responsible'] = self.request.user.pk
        return form

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Error in {field}: {error}")
        return render(self.request, self.template_name, self.get_context_data(form=form))
"""

'''
class TaskPageView(LoginRequiredMixin, TaskFormMixin, ListView):
    template_name = 'index_tasks.html'
    context_object_name = 'table_content'
    context_extra = {
        'title': 'Tasks',
        'table_headers': ['ID', 'Status', 'Labels', 'Creator', 
                         'Responsible', 'Description', 'Actions'],
        'form_action': 'task_create',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.context_extra)
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            task = form.save(commit=False)
            task.creator = request.user
            if not request.user.is_staff:
                task.responsible = request.user
            task.save()
            form.save_m2m()
            messages.success(request, 'Task created successfully')
            return redirect('tasks')
        return self.form_invalid(form)
'''

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

"""
class TaskUpdatePageView(LoginRequiredMixin, TaskModifyMixin, TaskFormMixin, UpdateView):
"""
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

    '''
    template_name = 'update.html'
    action = 'modify'

    def form_valid(self, form):
        if not self.request.user.is_staff:
            form.instance.responsible = self.request.user
        messages.success(self.request, 'Task updated successfully')
        return super().form_valid(form)
    '''

"""
class TaskDeletePageView(LoginRequiredMixin, TaskModifyMixin, DeleteView):
"""
class TaskDeletePageView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks')
    # action = 'delete'
    
    def get(self, request, *args, **kwargs):
        """Override get to handle deletion without template"""
        return self.delete(request, *args, **kwargs)