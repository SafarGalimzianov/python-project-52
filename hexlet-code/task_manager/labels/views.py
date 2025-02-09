# task_manager/labels/views.py
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from task_manager.labels.models import Label
from task_manager.labels.forms import LabelForm
from django.contrib import messages
from django.shortcuts import redirect
from django.db import IntegrityError

class LabelPageView(ListView):
    template_name = 'labels/index.html'
    model = Label
    context_object_name = 'labels'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields_name'] = ['ID', 'Label']
        return context

class LabelCreatePageView(CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'create.html'
    success_url = reverse_lazy('labels')

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except IntegrityError:
            messages.error(self.request, "Label with this name already exists.", extra_tags='warning')
            return self.form_invalid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Error in {field}: {error}")
        return super().form_invalid(form)

class LabelUpdatePageView(UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'update.html'
    success_url = reverse_lazy('labels')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form()
        context['form_fields'] = zip(form.fields.keys(), [field.label for field in form.fields.values()])
        context['field_name'] = 'label'
        return context

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except IntegrityError:
            messages.error(self.request, "Label with this name already exists.", extra_tags='warning')
            return self.form_invalid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Error in {field}: {error}")
        return super().form_invalid(form)

class LabelDeletePageView(DeleteView):
    model = Label
    success_url = reverse_lazy('labels')
    template_name = 'delete.html'

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)