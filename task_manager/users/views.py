from django.contrib import messages
from django.shortcuts import reverse, redirect
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from task_manager.users.forms import User
from django.contrib.auth.models import User as DjangoUser
from task_manager.users.forms import UserUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth import login
from task_manager.users.mixins import UserFormMixin


class UserLoginView(LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'action': reverse('login'),
        })
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Вы залогинены', extra_tags='.alert')
        return response

    def form_invalid(self, form):
        flash_messages = {
            'username_does_not_exist': 'Please enter a valid username',
            'password_invalid': 'Please use a correct password',
            'something_wrong': 'Something went wrong, please try again',
        }
        if form.errors.get('password'):
            messages.error(self.request, flash_messages['password_invalid'], extra_tags='warning')
        if form.errors.get('username'):
            messages.error(self.request, flash_messages['username_does_not_exist'], extra_tags='warning')
        if form.non_field_errors():
            messages.error(self.request, flash_messages['something_wrong'], extra_tags='warning')

        return super().form_invalid(form)
    
    next_page = reverse_lazy('home')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, 'Вы разлогинены', extra_tags='.alert')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        messages.success(self.request, 'Вы разлогинены', extra_tags='.alert')
        return super().get_context_data(**kwargs)


class UserPageView(ListView):
    template_name = 'users/index_users.html'
    context_object_name = 'table_content'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_headers'] = ['ID', 'Username']
        return context
    # Because using proxy model DjangoUser
    # The table User just references DjangoUser
    def get_queryset(self):
        return DjangoUser.objects.all()


class UserCreatePageView(UserFormMixin, CreateView):
    template_name = 'create.html'
    form_class = UserCreationForm
    context_extra = {
        'header': 'Users',
        'fields_names': ['ID', 'username'],
        # 'form_action': 'users_create',
    }
    success_url = reverse_lazy('users')


class UserUpdatePageView(UserFormMixin, UpdateView):
    model = DjangoUser
    template_name = 'update.html'
    success_url = reverse_lazy('users')
    form_class = UserUpdateForm
    context_extra = {
        'header': 'Users',
        'fields_names': ['ID', 'username'],
        # 'form_action': 'users_update',
    }

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)
    
    def form_invalid(self, form):
        if form.errors.get('username'):
            messages.error(self.request, 'Please use a different username', extra_tags='warning')
        if form.non_field_errors():
            messages.error(self.request, form.non_field_errors(), extra_tags='warning')
        return super().form_invalid(form)


class UserDeletePageView(DeleteView):
    model = DjangoUser
    success_url = reverse_lazy('users')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
