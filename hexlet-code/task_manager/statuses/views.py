from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from task_manager.statuses.models import Status
from task_manager.statuses.forms import StatusForm
from django.contrib import messages

class StatusPageView(ListView):
    template_name = 'index_statuses.html'
    model = Status
    context_object_name = 'statuses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields_name'] = ['ID', 'Status']
        return context

class StatusCreatePageView(CreateView):
    model = Status
    fields = ['status']
    template_name = 'create.html'
    success_url = reverse_lazy('statuses')


    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f"Error creating status: {e}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Error in {field}: {error}")
        return super().form_invalid(form)

class StatusUpdatePageView(UpdateView):
    model = Status
    template_name = 'update.html'
    success_url = reverse_lazy('statuses')
    form_class = StatusForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form()
        context['form_fields'] = zip(form.fields.keys(), [field.label for field in form.fields.values()])
        context['field_name'] = 'status'
        return context

class StatusDeletePageView(DeleteView):
    model = Status
    template_name = 'delete.html'
    success_url = reverse_lazy('statuses')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)