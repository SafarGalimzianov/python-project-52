from django.shortcuts import render, reverse
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
# from django.contrib.auth.forms import UserCreationForm
from task_manager.users.models import User
from django.urls import reverse_lazy
from django.contrib import messages

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
    template_name = 'index_users.html'
    model = User
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['field_names'] = ['ID', 'Username', 'Email']
        return context

class UserCreatePageView(CreateView):
    model = User
    fields = ['username', 'email', 'password']
    labels = ['Username', 'Email', 'Password']
    template_name = 'create.html'
    success_url = reverse_lazy('users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_fields'] = zip(self.fields, self.labels)
        return context
    
    def form_invalid(self, form):
        flash_messages = {
            'email_invalid': 'Please enter a valid email',
            'email_exists': 'Please enter a different email',
            'username_exists': 'Please use a different username',
        }
        if 'email' in form.errors:
            for error in form.errors['email']:
                if 'Enter a valid email address' in error:
                    messages.error(self.request, flash_messages['email_invalid'], extra_tags='warning')
                elif 'exists' in error:
                    messages.error(self.request, flash_messages['email_exists'], extra_tags='warning')
        if 'username' in form.errors:
            for error in form.errors['username']:
                if 'already exists' in error:
                    messages.error(self.request, flash_messages['username_exists'], extra_tags='warning')

        return super().form_invalid(form)

class UserUpdatePageView(UpdateView):
    model = User
    fields = ['username', 'email']
    template_name = 'update.html'
    success_url = reverse_lazy('users')

class UserDeletePageView(DeleteView):
    model = User
    template_name = 'delete.html'
    success_url = reverse_lazy('users')