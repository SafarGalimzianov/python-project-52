from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from task_manager.labels.models import Label
from task_manager.labels.mixins import LabelFormMixin

class LabelPageView(LabelFormMixin, ListView):
    template_name = 'labels/test.html'
    context_object_name = 'table_content'
    context_extra = {
        'title': 'Labels',
        'table_headers': ['ID', 'Label', 'Actions'],
        'form_action': 'label_create',
        }


class LabelCreatePageView(LabelFormMixin, CreateView):
    # Never rendered. Only because required by CreateView
    template_name = 'labels/create_labels.html'
    success_url = reverse_lazy('labels')

    def form_valid(self, form):
        messages.success(self.request, 'Ярлык успешно создан', extra_tags='.alert')
        # messages.success(self.request, f'{form.instance.label} created successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Error in {field}: {error}")
        return redirect('labels')


class LabelUpdatePageView(LabelFormMixin, UpdateView):
    template_name = 'labels/update_labels.html'
    success_url = reverse_lazy('labels')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        self.original_label = obj.name
        return obj

    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно изменен', extra_tags='.alert')
        '''
        messages.success(
            self.request,
            f'{self.original_label} updated to {form.instance.label} successfully'
        )
        '''
        return super().form_valid(form)


class LabelDeletePageView(DeleteView):
    model = Label
    template_name = 'delete.html'
    success_url = reverse_lazy('labels')
    context_extra = {
        'header': 'Labels',
        'fields_names': ['ID', 'name'],
    }

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, 'Ярлык успешно удален', extra_tags='.alert')
        return super().dispatch(request, *args, **kwargs)

    '''
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.tasks.exists():
            messages.error(self.request, "Cannot delete label because it is assigned to a task.")
            return redirect('labels')
        messages.success(self.request, f'{self.object.label} deleted successfully')
        return super().delete(request, *args, **kwargs)
    '''