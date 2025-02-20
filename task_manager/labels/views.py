from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from task_manager.labels.models import Label
from task_manager.labels.forms import LabelForm


class LabelFormMixin(FormMixin):
    model = Label
    form_class = LabelForm
    context_extra = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context.update(self.context_extra)
        return context


class LabelPageView(LabelFormMixin, ListView):
    template_name = 'index_labels.html'
    context_object_name = 'table_content'
    context_extra = {
        'title': 'Labels',
        'table_headers': ['ID', 'Label', 'Actions'],
        'form_action': 'label_create',
        }


class LabelCreatePageView(LabelFormMixin, CreateView):
    template_name = 'create.html' # Never rendered.Only because required by CreateView
    success_url = reverse_lazy('labels')

    def form_valid(self, form):
        messages.success(self.request, f'{form.instance.label} created successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Error in {field}: {error}")
        return redirect('labels')


class LabelUpdatePageView(LabelFormMixin, UpdateView):
    template_name = 'update.html'
    success_url = reverse_lazy('labels')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        self.original_label = obj.label
        return obj

    def form_valid(self, form):
        messages.success(
            self.request,
            f'{self.original_label} updated to {form.instance.label} successfully'
        )
        return super().form_valid(form)


class LabelDeletePageView(DeleteView):
    model = Label
    success_url = reverse_lazy('labels')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.tasks.exists():
            messages.error(self.request, "Cannot delete label because it is assigned to a task.")
            return redirect('labels')
        messages.success(self.request, f'{self.object.label} deleted successfully')
        return super().delete(request, *args, **kwargs)
