from django.urls import path

from task_manager.statuses import views

urlpatterns = [
    path('', views.StatusPageView.as_view(), name='statuses'),
    path('create/', views.StatusCreatePageView.as_view(), name='status_create'),
    path('<int:pk>/update/', views.StatusUpdatePageView.as_view(), name='status_update'),
    path('<int:pk>/delete/', views.StatusDeletePageView.as_view(), name='status_delete'),
]
