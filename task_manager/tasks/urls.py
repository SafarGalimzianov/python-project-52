from django.urls import path
from task_manager.tasks import views

urlpatterns = [
    path('', views.TaskPageView.as_view(), name='tasks'),
    path('create/', views.TaskCreatePageView.as_view(), name='task_create'),
    path('<int:pk>/', views.TaskShowPageView.as_view(), name='task_show'),
    path(
        '<int:pk>/update/',
        views.TaskUpdatePageView.as_view(),
        name='task_update'
     ),
    path(
        '<int:pk>/delete/',
        views.TaskDeletePageView.as_view(),
        name='task_delete'
     ),
]
