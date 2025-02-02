"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from task_manager import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('tasks/', views.TaskPageView.as_view(), name='tasks'),
    path('tasks/create/', views.TaskCreatePageView.as_view(), name='task_create'),
    path('tasks/<int:task_id>/update/', views.TaskUpdatePageView.as_view(), name='task_update'),
    path('tasks/<int:task_id>/delete/', views.TaskDeletePageView.as_view(), name='task_delete'),
    path('users/', include('task_manager.users.urls'), name='users'),
    path('statuses/', include('task_manager.statuses.urls'), name='statuses'),
    path('labels/', include('task_manager.labels.urls'), name='labels'),
]
