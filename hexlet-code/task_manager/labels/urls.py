from django.urls import path

from task_manager.labels import views

urlpatterns = [   
    path('', views.LabelPageView.as_view(), name='labels'),
    path('create/', views.LabelCreatePageView.as_view(), name='label_create'),
    path('<int:pk>/update/', views.LabelUpdatePageView.as_view(), name='label_update'),
    path('<int:pk>/delete/', views.LabelDeletePageView.as_view(), name='label_delete'),
]
