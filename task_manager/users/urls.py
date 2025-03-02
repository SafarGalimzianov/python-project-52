from django.urls import path

from task_manager.users import views

urlpatterns = [
    path('', views.UserPageView.as_view(), name='users'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('create/', views.UserCreatePageView.as_view(), name='users_create'),
    path('<int:pk>/update/', views.UserUpdatePageView.as_view(), \
         name='users_update'),
    path('<int:pk>/delete/', views.UserDeletePageView.as_view(), \
         name='users_delete'),
]
