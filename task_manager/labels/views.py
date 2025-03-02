from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import \
    ListView, CreateView, UpdateView, DeleteView
from task_manager.labels.models import Label
from task_manager.labels.mixins import LabelFormMixin
from task_manager.common.messages import LABEL_MESSAGES
import logging

logger = logging.getLogger(__name__)

class LabelPageView(LabelFormMixin, ListView):
    template_name = 'labels/index_labels.html'
    context_object_name = 'table_content'
    context_extra = {
        'title': 'Labels',
        'table_headers': ['ID', 'Label', 'Actions'],
        'form_action': 'label_create',
        'button_create': 'Создать метку',
    }

class LabelCreatePageView(LabelFormMixin, CreateView):
    template_name = 'create.html'
    success_url = reverse_lazy('labels')
    context_extra = {
        'header': 'Statuses',
        'button': 'Создать',
    }
    messages_show = {
        'error': LABEL_MESSAGES['create_error'],
        'success': LABEL_MESSAGES['create'],
    }

    def form_valid(self, form):
        messages.success(
            self.request,
            f'{self.messages_show["success"]}: {form.instance.name}',
            extra_tags='.alert'
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

class LabelUpdatePageView(LabelFormMixin, UpdateView):
    template_name = 'update.html'
    success_url = reverse_lazy('labels')
    messages_show = {
        'success': LABEL_MESSAGES['update'],
    }

    def form_valid(self, form):
        messages.success(
            self.request,
            self.messages_show['success'],
            extra_tags='.alert',
        )
        return super().form_valid(form)

class LabelDeletePageView(DeleteView):
    model = Label
    template_name = 'delete.html'
    success_url = reverse_lazy('labels')
    context_extra = {
        'header': 'Labels',
        'fields_names': ['ID', 'name'],
    }
    messages_show = {
        'error': LABEL_MESSAGES['delete_error'],
        'success': LABEL_MESSAGES['delete'],
    }

    def post(self, request, *args, **kwargs):
        object_to_delete = self.get_object()
        has_related_task = object_to_delete.tasks.exists()

        if has_related_task:
            logger.info(f'{request.user} CANNOT delete label \
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
                    LabelDeletePageView dispatch method')
        return super().dispatch(request, *args, **kwargs)
