from django.urls import path

from task_manager.statuses import views

urlpatterns = [
    path('', views.StatusPageView.as_view(), name='statuses'),
    path('create/', views.StatusCreatePageView.as_view(), name='status_create'),
    path('<int:status_id>/update/', views.StatusUpdatePageView.as_view(), name='status_update'),
    path('<int:status_id>/delete/', views.StatusDeletePageView.as_view(), name='status_delete'),
]
