'''
FilterSet Inheritance:
The class TaskFilter inherits from django_filters.FilterSet. This makes it a container for filter fields, which you can later use to filter your Task queryset.

Standard Filters:
You define several filters directly:

status: Filters tasks based on a related Status model object.
creator and responsible: Allow filtering by the User associated with task creation or responsibility.
description: Uses the icontains lookup to filter tasks whose description includes a substring.
labels: Allows filtering tasks by one or more Label objects.
These filters automatically build the right queryset conditions for most straightforward filters by matching model fields.

Custom Filter Method (q):

The q filter is a custom character filter (CharFilter) that uses the method filter_by_q.
Within filter_by_q, the code uses Django’s Q objects to combine conditions with an OR operator.
This means that if the search term is found in either the task’s description or in one of its labels (via the label's text), the task will be included in the results.
For example:

def filter_by_q(self, queryset, name, value):
    return queryset.filter(
        Q(description__icontains=value) | Q(labels__label__icontains=value)
    )

This custom filter lets you search across multiple fields – showing tasks where either the description or a label includes the search string.

Meta Class:
The inner class Meta specifies:

model: The Task model for which this filter is built.
fields: A list of fields that can be filtered. This tells django-filter which default filters to include alongside your custom ones.
In summary, the filters provide a way to narrow down the Task objects based on several criteria (status, creator, responsible, description, and labels) and support a special search field
(q) that pulls in tasks matching in either the description or their labels.
'''

import django_filters
from django.db.models import Q
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.contrib.auth import get_user_model
from django.forms import CheckboxInput
import logging

logger = logging.getLogger(__name__)

User = get_user_model()



class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(queryset=Status.objects.all(), label='Status')
    creator = django_filters.ModelChoiceFilter(queryset=User.objects.all(), label='Creator')
    executor = django_filters.ModelChoiceFilter(queryset=User.objects.all(), label='Executor')
    description = django_filters.CharFilter(lookup_expr='icontains', label='Description')
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label='Label',
        method='filter_by_label'
    )
    self_tasks = django_filters.BooleanFilter(
        method='filter_by_self_tasks',
        label='Only my tasks',
        widget=CheckboxInput
    )

    class Meta:
        model = Task
        fields = ['status', 'creator', 'executor', 'description', 'labels', 'self_tasks']

    def filter_by_self_tasks(self, queryset, name, value):
        logger.info(f"Self tasks filter called: value={value}, user={self.request.user if self.request else 'No request'}")
        if value:
            return queryset.filter(creator=self.request.user)
        return queryset

    def filter_by_label(self, queryset, name, value):
        logger.info(f"Label filter called: value={value}")
        if value:
            filtered_queryset = queryset.filter(labels=value)
            logger.info(f"Filtered queryset count: {filtered_queryset.count()}")
            return filtered_queryset
        return queryset