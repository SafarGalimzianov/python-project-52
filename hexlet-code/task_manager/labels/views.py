from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from task_manager.labels.models import Label

# Create your views here.

class LabelPageView(ListView):
    template_name = 'labels/index.html'
    model = Label
    context_object_name = 'labels'

class LabelCreatePageView(CreateView):
    model = Label
    fields = ['label']
    template_name = 'create.html'
    success_url = reverse_lazy('labels')

class LabelUpdatePageView(UpdateView):
    model = Label
    fields = ['label']
    template_name = 'update.html'
    success_url = reverse_lazy('labels')

class LabelDeletePageView(DeleteView):
    model = Label
    template_name = 'delete.html'
    success_url = reverse_lazy('labels')

