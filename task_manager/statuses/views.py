from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import \
    ListView, CreateView, UpdateView, DeleteView
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.statuses.mixins import StatusFormMixin
from task_manager.common.messages import STATUS_MESSAGES
import logging

logger = logging.getLogger(__name__)

class StatusPageView(StatusFormMixin, ListView):
    template_name = 'statuses/test.html'
    context_object_name = 'table_content'
    context_extra = {
        'title': 'Statuses',
        'table_headers': ['ID', 'Status', 'Actions'],
        'form_action': 'status_create',
    }

class StatusCreatePageView(StatusFormMixin, CreateView):
    template_name = 'statuses/create_statuses.html'
    success_url = reverse_lazy('statuses')
    messages_show = {
        'error': STATUS_MESSAGES['create_error'],
        'success': STATUS_MESSAGES['create'],
    }

    def form_valid(self, form):
        messages.success(
            self.request,
            f'{self.messages_show["success"]}: {form.instance.name}',
            extra_tags='.alert',
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    self.request,
                    f'{self.messages_show["error"]}: {field}: {error}',
                    extra_tags='.alert',
                )
        return redirect(self.success_url)

class StatusUpdatePageView(StatusFormMixin, UpdateView):
    template_name = 'update.html'
    success_url = reverse_lazy('statuses')
    messages_show = {
        'success': STATUS_MESSAGES['update'],
    }

    def form_valid(self, form):
        messages.success(
            self.request,
            self.messages_show['success'],
            extra_tags='.alert',
        )
        return super().form_valid(form)

class StatusDeletePageView(DeleteView):
    model = Status
    template_name = 'delete.html'
    success_url = reverse_lazy('statuses')
    context_extra = {
        'header': 'Statuses',
        'fields_names': ['ID', 'name'],
    }
    messages_show = {
        'error': STATUS_MESSAGES['delete_error'],
        'success': STATUS_MESSAGES['delete'],
    }

    def post(self, request, *args, **kwargs):
        object_to_delete = self.get_object()
        has_related_task = \
            Task.objects.filter(status=object_to_delete).exists()
        
        if has_related_task:
            logger.info(f'{request.user} CANNOT delete status \
                        {object_to_delete} - associated with tasks')
            messages.error(
                self.request,
                self.messages_show['error'],
                extra_tags='.alert',
            )
            return redirect(self.success_url)
        
        response = super().post(request, *args, **kwargs)
        messages.success(
            self.request,
            self.messages_show['success'],
            extra_tags='.alert',
        )
        return response
        
    def dispatch(self, request, *args, **kwargs):
        logger.info(f'{request.user} now in \
                    StatusDeletePageView dispatch method')
        return super().dispatch(request, *args, **kwargs)
