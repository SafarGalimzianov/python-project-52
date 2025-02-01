from django.urls import path

from task_manager.statuses import views

urlpatters = [
    path('', views.StatusPageView.as_view(), name='labels'),
    path('create/', views.StatusCreatePageView.as_view(), name='label_create'),
    path('<int:status_id>/update/', views.StatusUpdatePageView.as_view(), name='label_update'),
    path('<int:status_id>/delete/', views.StatusDeletePageView.as_view(), name='label_delete'),
]
