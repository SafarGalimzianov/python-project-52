from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from task_manager.statuses.models import Status

# Create your views here.

class StatusPageView(ListView):
    template_name = 'statuses/index.html'
    model = Status
    context_object_name = 'statuses'

class StatusCreatePageView(CreateView):
    model = Status
    fields = ['status']
    template_name = 'create.html'
    success_url = reverse_lazy('statuses')

class StatusUpdatePageView(UpdateView):
    model = Status
    fields = ['status']
    template_name = 'update.html'
    success_url = reverse_lazy('statuses')

class StatusDeletePageView(DeleteView):
    model = Status
    template_name = 'delete.html'
    success_url = reverse_lazy('statuses')

