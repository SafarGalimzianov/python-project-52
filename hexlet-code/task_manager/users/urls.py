from django.urls import path

from task_manager.users import views

urlpatters = [
    path('', views.UserPageView.as_view(), name='users'),
    path('create/', views.UserCreatePageView.as_view(), name='users_create'),
    path('<int:user_id>/update/', views.UserUpdatePageView.as_view(), name='users_update'),
    path('<int:user_id>/delete/', views.UserDeletePageView.as_view(), name='users_delete'),
]
