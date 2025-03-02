from django.contrib import messages
from django.shortcuts import reverse, redirect
from django.views.generic import \
    ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from task_manager.users.models import User
from task_manager.users.forms import UserCreateForm, UserUpdateForm
from django.urls import reverse_lazy
from task_manager.users.mixins import UserFormMixin
from task_manager.tasks.models import Task
from task_manager.common.messages import USER_MESSAGES
import logging

logger = logging.getLogger(__name__)


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = AuthenticationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'action': reverse('login'),
        })
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info(f'User {self.request.user} created {form.fields.items()}')
        messages.success(
            self.request,
            USER_MESSAGES['login'],
            extra_tags='.alert',
        )
        return response

    def form_invalid(self, form):
        if form.errors.get('password'):
            messages.error(
                self.request,
                USER_MESSAGES['password_error'],
                extra_tags='warning',
            )
        if form.errors.get('username'):
            messages.error(
                self.request,
                USER_MESSAGES['username_error'],
                extra_tags='warning',
            )
        if form.non_field_errors():
            messages.error(
                self.request,
                USER_MESSAGES['general_error'],
                extra_tags='warning',
            )

        return super().form_invalid(form)
    next_page = reverse_lazy('home')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        messages.success(
            self.request,
            USER_MESSAGES['logout'],
            extra_tags='.alert',
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        messages.success(
            self.request,
            USER_MESSAGES['logout'],
            extra_tags='.alert',
        )
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
        messages.success(
            self.request,
            USER_MESSAGES['create'],
            extra_tags='.alert',
        )
        return super().dispatch(request, *args, **kwargs)


class UserUpdatePageView(UserFormMixin, UpdateView):
    model = User
    template_name = 'update.html'
    success_url = reverse_lazy('users')
    form_class = UserUpdateForm
    context_extra = {
        'header': 'Users',
        'fields_names': [
            'ID',
            'username',
            'first_name',
            'last_name',
            'password',
            'password1',
            'password2',
        ],
    }

    def dispatch(self, request, *args, **kwargs):
        logger.info(f'User {self.get_object()} \
                    updated by {self.request.user}')
        messages.success(
            self.request,
            USER_MESSAGES['update'],
            extra_tags='.alert',
        )
        return super().dispatch(request, *args, **kwargs)
    
    def form_invalid(self, form):
        logger.info(f'User {self.request.user} updated {self.get_object()}')
        if form.errors.get('username'):
            messages.error(
                self.request,
                'Please use a different username',
                extra_tags='.alert',
            )
        if form.non_field_errors():
            messages.error(
                self.request,
                form.non_field_errors(),
                extra_tags='.alert',
            )
        return super().form_invalid(form)


class UserDeletePageView(DeleteView):
    model = User
    template_name = 'delete.html'
    success_url = reverse_lazy('users')
    context_extra = {
        'header': 'Users',
        'fields_names': [
            'ID',
            'username',
            'first_name',
            'last_name',
            'password',
            'password1',
            'password2',
        ],
    }
    
    def get(self, request, *args, **kwargs):
        object_to_delete = self.get_object()
        has_tasks_as_creator = \
            Task.objects.filter(creator=object_to_delete).exists()
        has_tasks_as_executor = \
            Task.objects.filter(executor=object_to_delete).exists()

        if request.user.id != object_to_delete.id:
            logger.info(f'{request.user} CANNOT delete user \
                        {object_to_delete} - NOT SAME user')
            messages.error(
                self.request,
                USER_MESSAGES['permission_error'],
                extra_tags='.alert'
            )
            return redirect(self.success_url)
        elif has_tasks_as_creator or has_tasks_as_executor:
            logger.info(f'User {request.user} CANNOT delete user \
                        {object_to_delete} IS associated with tasks')
            messages.error(
                self.request,
                USER_MESSAGES['delete_error'],
                extra_tags='.alert'
            )
            return redirect(self.success_url)
        else:
            logger.info(f'{request.user} CAN delete user \
                        {object_to_delete} SAME and NOT \
                            associated with tasks')
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.success(
            self.request,
            USER_MESSAGES['delete'],
            extra_tags='.alert',
        )
        return response
        
    def dispatch(self, request, *args, **kwargs):
        logger.info(f"{request.user} now in \
                    UserDeletePageView dispatch method")
        return super().dispatch(request, *args, **kwargs)
