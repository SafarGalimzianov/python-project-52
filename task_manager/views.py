from task_manager.tasks.models import Task
from task_manager.filters import TaskFilter
from django_filters.views import FilterView


class HomePageView(FilterView):
    model = Task
    filterset_class = TaskFilter
    template_name = 'home.html'
    context_object_name = 'tasks'
