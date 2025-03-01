from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.statuses.mixins import StatusFormMixin
import logging

logger = logging.getLogger(__name__)

class StatusPageView(StatusFormMixin, ListView):
    # template_name = 'statuses/index_statuses.html'
    template_name = 'statuses/test.html'
    context_object_name = 'table_content'
    context_extra = {
        'title': 'Statuses',
        'table_headers': ['ID', 'Status', 'Actions'],
        'form_action': 'status_create',
    }

class StatusCreatePageView(StatusFormMixin, CreateView):
    # template_name = 'create.html'
    template_name = 'statuses/create_statuses.html'
    success_url = reverse_lazy('statuses')

    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно создан', extra_tags='.alert')
        # messages.success(self.request, f'{form.instance.status} created successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Error in {field}: {error}")
        return redirect('statuses')
    '''
    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, 'Статус успешно создан', extra_tags='.alert')
        return super().dispatch(request, *args, **kwargs)
    '''

class StatusUpdatePageView(StatusFormMixin, UpdateView):
    # template_name = 'update.html'
    template_name = 'statuses/update_statuses.html'
    success_url = reverse_lazy('statuses')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        self.original_status = obj.name
        return obj

    def form_valid(self, form):
        # Calling super().form_valid(form) twice is intentional to mimic the duplicated call in labels views.
        '''
        response = super().form_valid(form)
        messages.success(self.request, f'{self.original_status} updated to {form.instance.status} successfully')
        '''
        messages.success(self.request, 'Статус успешно изменен', extra_tags='.alert')
        return super().form_valid(form)


class StatusDeletePageView(DeleteView):
    model = Status
    template_name = 'delete.html'
    success_url = reverse_lazy('statuses')
    context_extra = {
        'header': 'Statuses',
        'fields_names': ['ID', 'name'],
    }

    def get(self, request, *args, **kwargs):
        status_to_delete = self.get_object()
        has_related_task = Task.objects.filter(status=status_to_delete).exists()

        if has_related_task:
            logger.info(f"{request.user} CANNOT delete status {status_to_delete} - associated with tasks")
            messages.error(
                self.request,
                'Невозможно удалить статус, потому что он используется',
                extra_tags='.alert'
            )
            return redirect(self.success_url)
        else:
            logger.info(f"{request.user} CAN delete status {status_to_delete} - NOT associated with tasks")
            # Show confirmation page if it's the same user and no tasks
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Check again before actually deleting (to handle race conditions)
        status_to_delete = self.get_object()
        has_related_task = Task.objects.filter(status=status_to_delete).exists()

        if has_related_task:
            logger.info(f"{request.user} CANNOT delete status {status_to_delete} - associated with tasks")
            messages.error(
                self.request,
                'Невозможно удалить статус, потому что он используется',
                extra_tags='.alert'
            )
            return redirect(self.success_url)
        
        response = super().post(request, *args, **kwargs)
        messages.success(self.request, 'Статус успешно удален', extra_tags='.alert')
        return response

    def dispatch(self, request, *args, **kwargs):
        logger.info(f"{request.user} now in statuses/ StatusDeletePageView dispatch method")
        return super().dispatch(request, *args, **kwargs)
