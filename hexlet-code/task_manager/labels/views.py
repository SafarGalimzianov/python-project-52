from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from task_manager.labels.models import Label
from task_manager.labels.forms import LabelForm

class LabelPageView(FormMixin, ListView):
    template_name = 'index_labels.html'  
    model = Label
    form_class = LabelForm
    context_object_name = 'table_content'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Labels'
        context['form'] = self.get_form()
        context['table_headers'] = ['ID', 'Label', 'Actions']
        return context

class LabelCreatePageView(CreateView):
    model = Label
    form_class = LabelForm
    success_url = reverse_lazy('labels')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def form_valid(self, form):
        messages.success(self.request, f'{form.instance.label} created successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Error in {field}: {error}")
        return super().form_invalid(form)

class LabelUpdatePageView(UpdateView):
    template_name = 'update.html'
    model = Label
    form_class = LabelForm
    success_url = reverse_lazy('labels')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

class LabelDeletePageView(DeleteView):
    model = Label
    success_url = reverse_lazy('labels')