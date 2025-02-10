from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from task_manager.labels.models import Label
from task_manager.labels.forms import LabelForm
from django.contrib import messages

class LabelPageView(ListView):
    template_name = 'index_labels.html'  
    model = Label
    context_object_name = 'labels'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields_name'] = ['ID', 'Label']
        context['form'] = LabelForm()
        return context

class LabelCreatePageView(CreateView):
    model = Label
    fields = ['label']
    template_name = 'create.html'
    success_url = reverse_lazy('labels')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_fields'] = zip(self.get_form().fields.keys(), 
                                   [field.label for field in self.get_form().fields.values()])
        context['form'] = LabelForm()
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Label created successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Error in {field}: {error}")
        return super().form_invalid(form)

class LabelUpdatePageView(UpdateView):
    model = Label
    template_name = 'update.html'
    success_url = reverse_lazy('labels')
    form_class = LabelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form()
        context['form_fields'] = zip(form.fields.keys(), 
                                   [field.label for field in form.fields.values()])
        context['field_name'] = 'label'
        return context

class LabelDeletePageView(DeleteView):
    model = Label
    template_name = 'delete.html'
    success_url = reverse_lazy('labels')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)