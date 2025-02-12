# python
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from task_manager.models import Task
from task_manager.users.models import User
from task_manager.forms import TaskForm

class HomePageView(TemplateView):
    template_name = 'home.html'

class SearchPageView:
    template_name = 'search.html'


class TaskFormMixin(FormMixin):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks')
    context_extra = {
        'fields_names': ['ID', 'Status', 'Labels', 'Creator', 
                        'Responsible', 'Description', 'Actions']
    }

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

class TaskModifyMixin:
    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if task.creator != request.user:
            messages.error(request, f'Only the creator can {self.action} the task')
            return redirect('tasks')
        return super().dispatch(request, *args, **kwargs)

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

class TaskCreatePageView(LoginRequiredMixin, TaskFormMixin, CreateView):
    template_name = 'create.html'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        if not self.request.user.is_staff:
            form.instance.responsible = self.request.user
        messages.success(self.request, 'Task created successfully')
        return super().form_valid(form)

class TaskUpdatePageView(LoginRequiredMixin, TaskModifyMixin, TaskFormMixin, UpdateView):
    template_name = 'update.html'
    action = 'modify'

    def form_valid(self, form):
        if not self.request.user.is_staff:
            form.instance.responsible = self.request.user
        messages.success(self.request, 'Task updated successfully')
        return super().form_valid(form)

class TaskDeletePageView(LoginRequiredMixin, TaskModifyMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks')
    action = 'delete'
    
    def get(self, request, *args, **kwargs):
        """Override get to handle deletion without template"""
        return self.delete(request, *args, **kwargs)