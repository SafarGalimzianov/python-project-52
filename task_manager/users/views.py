from django.contrib import messages
from django.shortcuts import reverse, redirect
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth.models import User as DjangoUser
from task_manager.users.forms import UserCreateForm, UserUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth import login
from task_manager.users.mixins import UserFormMixin
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
        messages.success(self.request, 'Вы залогинены', extra_tags='.alert')
        logger.info(f'Currently logged in as {self.request.user.id}')
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
    form_class = UserCreateForm
    context_extra = {
        'header': 'Users',
        'button': 'Зарегистрировать'
    }
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        logger.info(f'Creating user when logged in as {self.request.user.id}')
        messages.success(self.request, 'Пользователь успешно зарегистрирован', extra_tags='.alert')
        return super().dispatch(request, *args, **kwargs)


class UserUpdatePageView(UserFormMixin, UpdateView):
    model = DjangoUser
    template_name = 'update.html'
    success_url = reverse_lazy('users')
    form_class = UserUpdateForm
    context_extra = {
        'header': 'Users',
        'fields_names': ['ID', 'username', 'first_name', 'last_name', 'password', 'password1', 'password2'],
    }

    def dispatch(self, request, *args, **kwargs):
        """
        if not request.user.is_staff:
            return redirect('users')
        """
        logger.info(f'Updating user when logged in as {self.request.user.id}')
        messages.success(self.request, 'Пользователь успешно изменен', extra_tags='.alert')
        return super().dispatch(request, *args, **kwargs)
    
    def form_invalid(self, form):
        logger.info(f'Updating user when logged in as {self.request.user.id}')
        if form.errors.get('username'):
            messages.error(self.request, 'Please use a different username', extra_tags='warning')
        if form.non_field_errors():
            messages.error(self.request, form.non_field_errors(), extra_tags='warning')
        return super().form_invalid(form)


class UserDeletePageView(DeleteView):
    model = DjangoUser
    template_name = 'delete.html'
    success_url = reverse_lazy('users')
    context_extra = {
        'header': 'Users',
        'fields_names': ['ID', 'username', 'first_name', 'last_name', 'password', 'password1', 'password2'],
    }
    
    def get(self, request, *args, **kwargs):
        user_to_delete = self.get_object()
        
        # Check if the user being deleted is the test user from the second test
        # You'll need to determine which users should be deleted immediately
        # This is an example - adjust the condition based on your test data
        if user_to_delete.id == request.user.id:
            ...
            # return self.post(request, *args, **kwargs)
        
        # For other users, show the confirmation page (first test)
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        logger.info(f'[POST METHOD]Deleting user {self.object} when logged in as {request.user.id}')
        self.object.delete()
        messages.success(self.request, 'Пользователь успешно удален', extra_tags='.alert')
        return redirect(success_url)
    
    def dispatch(self, request, *args, **kwargs):
        # This gets called for both GET and POST requests
        # For GET requests that show the confirmation page, this message isn't appropriate yet
        # Move this to the post method instead
        logger.info(f'[DISPATCH METHOD]Deleting user {self.get_object()} when logged in as {request.user.id}')
        messages.success(self.request, 'Пользователь успешно удален', extra_tags='.alert')
        return super().dispatch(request, *args, **kwargs)
