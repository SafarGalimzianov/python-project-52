from task_manager.common.views import \
    BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView
from task_manager.statuses.models import Status
from task_manager.statuses.mixins import StatusFormMixin
from task_manager.tasks.models import Task
from task_manager.common.messages import STATUS_MESSAGES
from django.urls import reverse_lazy
import logging

logger = logging.getLogger(__name__)


class StatusPageView(StatusFormMixin, BaseListView):
    template_name = 'statuses/index_statuses.html'
    context_extra = {
        'title': 'Statuses',
        'table_headers': ['ID', 'Status', 'Actions'],
        'form_action': 'status_create',
        'button_create': 'Создать статус',
    }


class StatusCreatePageView(StatusFormMixin, BaseCreateView):
    success_url = reverse_lazy('statuses')
    context_extra = {
        'header': 'Statuses',
        'button': 'Создать',
    }
    messages_show = {
        'error': STATUS_MESSAGES['create_error'],
        'success': STATUS_MESSAGES['create'],
    }


class StatusUpdatePageView(StatusFormMixin, BaseUpdateView):
    success_url = reverse_lazy('statuses')
    messages_show = {
        'success': STATUS_MESSAGES['update'],
    }


class StatusDeletePageView(BaseDeleteView):
    model = Status
    success_url = reverse_lazy('statuses')
    context_extra = {
        'header': 'Statuses',
        'fields_names': ['ID', 'name'],
    }
    messages_show = {
        'error': STATUS_MESSAGES['delete_error'],
        'success': STATUS_MESSAGES['delete'],
    }
    
    def has_related_objects(self):
        return Task.objects.filter(status=self.get_object()).exists()
    
    def dispatch(self, request, *args, **kwargs):
        logger.info(f'{request.user} in StatusDeletePageView dispatch')
        return super().dispatch(request, *args, **kwargs)
