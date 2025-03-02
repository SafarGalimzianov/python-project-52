from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import \
    ListView, CreateView, UpdateView, DeleteView
from task_manager.labels.models import Label
from task_manager.labels.mixins import LabelFormMixin
import logging

logger = logging.getLogger(__name__)

class LabelPageView(LabelFormMixin, ListView):
    template_name = 'labels/test.html'
    context_object_name = 'table_content'
    context_extra = {
        'title': 'Labels',
        'table_headers': ['ID', 'Label', 'Actions'],
        'form_action': 'label_create',
        }


class LabelCreatePageView(LabelFormMixin, CreateView):
    template_name = 'labels/create_labels.html'
    success_url = reverse_lazy('labels')
    messages_show = {
        'error': 'Ошибка при создании метки',
        'success': 'Метка успешно создана',
    }

    def form_valid(self, form):
        messages.success(
            self.request,
            f'{self.messages_show['success']}: {form.instance.name}',
            extra_tags='.alert'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    self.request,
                    f'{self.messages_show['error']}: {field}: {error}',
                    extra_tags='.alert',
                )
        return redirect('labels')


class LabelUpdatePageView(LabelFormMixin, UpdateView):
    template_name = 'labels/update_labels.html'
    success_url = reverse_lazy('labels')
    messages_show = {
        'success': 'Метка успешно изменена',
    }

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        self.original_object = obj.name
        return obj

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
        'error': 'Невозможно удалить метку, потому что она используется',
        'success': 'Метка успешно удалена',
    }

    def post(self, request, *args, **kwargs):
        label_to_delete = self.get_object()
        has_related_task = label_to_delete.tasks.exists()

        if has_related_task:
            logger.info(f"{request.user} CANNOT delete label \
                        {label_to_delete} - associated with tasks")
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
        logger.info(f"{request.user} now in \
                    LabelDeletePageView dispatch method")
        return super().dispatch(request, *args, **kwargs)
