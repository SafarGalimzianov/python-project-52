from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from task_manager.models import Task
from task_manager.users.models import User
from task_manager.forms import TaskForm

class HomePageView(TemplateView):
    template_name = 'home.html'

class SearchPageView:
    template_name = 'search.html'


class TaskPageView(LoginRequiredMixin, ListView):
    template_name = 'index_tasks.html'
    model = Task
    context_object_name = 'tasks'

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.creator = request.user
            if not request.user.is_staff:
                task.responsible = request.user  
            task.save()
            form.save_m2m()
            messages.success(request, 'Task created successfully')
            return redirect('tasks')
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields_names'] = ['ID', 'Status', 'Labels', 'Creator', 
                                'Responsible', 'Description', 'Actions']
        form = TaskForm(initial={'responsible': self.request.user})  # Set initial value
        if not self.request.user.is_staff:
            form.fields['responsible'].disabled = True
        context['form'] = form
        return context
    

class TaskCreatePageView(LoginRequiredMixin, CreateView):
    template_name = 'create.html'
    model = Task
    fields = ['status', 'labels', 'responsible', 'description']
    success_url = reverse_lazy('tasks')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # For regular users, force responsible to current user and disable the field
        if not self.request.user.is_staff:
            form.fields['responsible'].disabled = True
            form.initial['responsible'] = self.request.user.pk
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form()
        context['form_fields'] = zip(form.fields.keys(),
                                     [field.label for field in form.fields.values()])
        context['form'] = form
        return context

    def form_valid(self, form):
        # Always set creator as current user
        form.instance.creator = self.request.user
        # For non-admin users, override responsible to current user
        if not self.request.user.is_staff:
            form.instance.responsible = self.request.user
        messages.success(self.request, 'Task created successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Error in {field}: {error}")
        return super().form_invalid(form)


class TaskUpdatePageView(LoginRequiredMixin, UpdateView):
    template_name = 'update.html'
    model = Task
    fields = ['status', 'labels', 'responsible', 'description']
    success_url = reverse_lazy('tasks')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # For regular users, disable changing the responsible field
        if not self.request.user.is_staff:
            form.fields['responsible'].disabled = True
            form.initial['responsible'] = self.request.user.pk
        return form

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if task.creator != request.user:
            messages.error(request, 'Only the creator can modify the task')
            return redirect('tasks')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form()
        context['form_fields'] = zip(
            form.fields.keys(),
            [field.label for field in form.fields.values()]
        )
        context['form'] = form
        return context

    def form_valid(self, form):
        # For non-admin users, force responsible to current user
        if not self.request.user.is_staff:
            form.instance.responsible = self.request.user
        messages.success(self.request, 'Task updated successfully')
        return super().form_valid(form)

class TaskDeletePageView(LoginRequiredMixin, DeleteView):
    template_name = 'delete.html'
    model = Task
    success_url = reverse_lazy('tasks')

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if task.creator != request.user:
            messages.error(request, 'Only the creator can delete the task')
            return redirect('tasks')
        return super().dispatch(request, *args, **kwargs)