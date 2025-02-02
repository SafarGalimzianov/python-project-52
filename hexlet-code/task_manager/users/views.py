from django.shortcuts import render, reverse
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from task_manager.users.models import User
from django.urls import reverse_lazy

# Create your views here.

class UserLoginView(LoginView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'action': reverse('login'),
        })
        return context

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')

class UserPageView(ListView):
    template_name = 'index.html'
    model = User
    context_object_name = 'users'

class UserCreatePageView(TemplateView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'action': reverse('users:create'),
            'is_register': True,
        })
        return context

class UserUpdatePageView(UpdateView):
    model = User
    fields = ['username', 'email']
    template_name = 'update.html'
    success_url = reverse_lazy('users')

class UserDeletePageView(DeleteView):
    model = User
    template_name = 'delete.html'
    success_url = reverse_lazy('users')