from django.contrib import messages
from django.shortcuts import reverse, redirect
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from task_manager.users.models import User
from task_manager.users.forms import UserCreateForm, UserUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth import login
from task_manager.users.mixins import UserFormMixin
from task_manager.tasks.models import Task
import logging

logger = logging.getLogger(__name__)


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
        logger.info(f'User {form.fields.items()} created by {self.request.user}')
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
    def get_queryset(self):
        return User.objects.all()

class UserCreatePageView(UserFormMixin, CreateView):
    template_name = 'create.html'
    form_class = UserCreateForm
    context_extra = {
        'header': 'Users',
        'button': 'Зарегистрировать'
    }
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        logger.info(f'Creating user when logged in as {request.user}')
        messages.success(self.request, 'Пользователь успешно зарегистрирован', extra_tags='.alert')
        return super().dispatch(request, *args, **kwargs)


class UserUpdatePageView(UserFormMixin, UpdateView):
    model = User
    template_name = 'update.html'
    success_url = reverse_lazy('users')
    form_class = UserUpdateForm
    context_extra = {
        'header': 'Users',
        'fields_names': ['ID', 'username', 'first_name', 'last_name', 'password', 'password1', 'password2'],
    }

    def dispatch(self, request, *args, **kwargs):
        logger.info(f'User {self.get_object()} updated by {self.request.user}')
        messages.success(self.request, 'Пользователь успешно изменен', extra_tags='.alert')
        return super().dispatch(request, *args, **kwargs)
    
    def form_invalid(self, form):
        logger.info(f'User {self.get_object()} updated by {self.request.user}')
        if form.errors.get('username'):
            messages.error(self.request, 'Please use a different username', extra_tags='.alert')
        if form.non_field_errors():
            messages.error(self.request, form.non_field_errors(), extra_tags='.alert')
        return super().form_invalid(form)


class UserDeletePageView(DeleteView):
    model = User
    template_name = 'delete.html'
    success_url = reverse_lazy('users')
    context_extra = {
        'header': 'Users',
        'fields_names': ['ID', 'username', 'first_name', 'last_name', 'password', 'password1', 'password2'],
    }
    
    def get(self, request, *args, **kwargs):
        user_to_delete = self.get_object()
        has_tasks_as_creator = Task.objects.filter(creator=user_to_delete).exists()
        has_tasks_as_executor = Task.objects.filter(executor=user_to_delete).exists()

        if request.user != user_to_delete:
            logger.info(f"{request.user} CANNOT delete user {user_to_delete} - NOT SAME user")
            message = 'У вас нет прав для изменения другого пользователя.'
            messages.error(
                self.request,
                message,
                extra_tags='.alert'
            )
            return redirect(self.success_url)
        elif has_tasks_as_creator or has_tasks_as_executor:
            logger.info(f"{request.user} CANNOT delete user {user_to_delete} - associated with tasks")
            messages.error(
                self.request,
                'Невозможно удалить пользователя, потому что он используется',
                extra_tags='.alert'
            )
            return redirect(self.success_url)
        else:
            logger.info(f"{request.user} CAN delete user {user_to_delete} - SAME user and NOT associated with tasks")
            # Show confirmation page if it's the same user and no tasks
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.success(self.request, 'Пользователь успешно удален', extra_tags='.alert')
        return response
        
    def dispatch(self, request, *args, **kwargs):
        logger.info(f"{request.user} now in users/ UserDeletePageView dispatch method")
        return super().dispatch(request, *args, **kwargs)
