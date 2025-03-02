from task_manager.common.views import \
    BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView
from task_manager.labels.models import Label
from task_manager.labels.mixins import LabelFormMixin
from task_manager.common.messages import LABEL_MESSAGES
from django.urls import reverse_lazy
import logging

logger = logging.getLogger(__name__)

class LabelPageView(LabelFormMixin, BaseListView):
    template_name = 'labels/index_labels.html'
    context_extra = {
        'title': 'Labels',
        'table_headers': ['ID', 'Метка', 'Действия'],
        'form_action': 'label_create',
        'button_create': 'Создать метку',
    }

class LabelCreatePageView(LabelFormMixin, BaseCreateView):
    success_url = reverse_lazy('labels')
    context_extra = {
        'header': 'Labels',
        'button': 'Создать',
    }
    messages_show = {
        'error': LABEL_MESSAGES['create_error'],
        'success': LABEL_MESSAGES['create'],
    }

class LabelUpdatePageView(LabelFormMixin, BaseUpdateView):
    success_url = reverse_lazy('labels')
    messages_show = {
        'success': LABEL_MESSAGES['update'],
    }

class LabelDeletePageView(BaseDeleteView):
    model = Label
    success_url = reverse_lazy('labels')
    context_extra = {
        'header': 'Labels',
        'fields_names': ['ID', 'name'],
    }
    messages_show = {
        'error': LABEL_MESSAGES['delete_error'],
        'success': LABEL_MESSAGES['delete'],
    }
    
    def has_related_objects(self):
        return self.get_object().tasks.exists()
    
    def dispatch(self, request, *args, **kwargs):
        logger.info(f'{request.user} in LabelDeletePageView dispatch')
        return super().dispatch(request, *args, **kwargs)
