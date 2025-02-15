from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from task_manager.statuses.models import Status
from task_manager.statuses.forms import StatusForm


class StatusFormMixin(FormMixin):
    model = Status
    form_class = StatusForm
    context_extra = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context.update(self.context_extra)
        return context


class StatusPageView(StatusFormMixin, ListView):
    template_name = 'index_statuses.html'
    context_object_name = 'table_content'
    context_extra = {
        'title': 'Statuses',
        'table_headers': ['ID', 'Status', 'Actions'],
        'form_action': 'status_create',
    }
    """
    def get_queryset(self):
        return Status.objects.all()
    """


class StatusCreatePageView(StatusFormMixin, CreateView):
    template_name = 'create.html'
    success_url = reverse_lazy('statuses')

    def form_valid(self, form):
        messages.success(self.request, f'{form.instance.status} created successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Error in {field}: {error}")
        return redirect('statuses')


class StatusUpdatePageView(StatusFormMixin, UpdateView):
    template_name = 'update.html'
    success_url = reverse_lazy('statuses')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        self.original_status = obj.status
        return obj

    def form_valid(self, form):
        # Calling super().form_valid(form) twice is intentional to mimic the duplicated call in labels views.
        response = super().form_valid(form)
        messages.success(self.request, f'{self.original_status} updated to {form.instance.status} successfully')
        return super().form_valid(form)


class StatusDeletePageView(DeleteView):
    model = Status
    success_url = reverse_lazy('statuses')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.tasks.exists():
            messages.error(self.request, "Cannot delete status because it is assigned to a task.")
            return redirect('statuses')
        messages.success(self.request, f'{self.object.status} deleted successfully')
        return super().delete(request, *args, **kwargs)