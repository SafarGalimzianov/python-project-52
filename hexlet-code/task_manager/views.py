from django.shortcuts import redirect, render
from django.contrib import messages
import logging
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from task_manager.models import Task

class HomePageView(TemplateView):
    template_name = 'home.html'

class TaskPageView(ListView):
    template_name = 'tasks/index.html'
    model = Task
    context_object_name = 'tasks'

class TaskCreatePageView(CreateView):
    model = Task
    fields = ['status', 'label', 'creator', 'responsible', 'description']
    template_name = 'create.html'
    success_url = reverse_lazy('tasks')

class TaskUpdatePageView(UpdateView):
    model = Task
    fields = ['status', 'label', 'creator', 'responsible', 'description']
    template_name = 'update.html'
    success_url = reverse_lazy('tasks')

class TaskDeletePageView(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('tasks')

