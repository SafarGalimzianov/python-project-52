from django.contrib import messages
from django.shortcuts import reverse, redirect
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from task_manager.users.models import User
from django.contrib.auth.models import User as DjangoUser
from task_manager.users.forms import UserUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth import login


class UserLoginView(LoginView):
    template_name = 'login.html'
    model = User
    form_class = AuthenticationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'action': reverse('login'),
        })
        return context
    
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
    
    def get_success_url(self):
        return reverse_lazy('home')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')


class UserPageView(ListView):
    template_name = 'users/index_users.html'
    model = User
    context_object_name = 'users'

    def get_queryset(self):
        return DjangoUser.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields_names'] = ['ID', 'username']
        # context['fields_names'] = [field.verbose_name for field in self.model._meta.fields]
        return context


class UserCreatePageView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'create.html'
    success_url = reverse_lazy('users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form()
        # Change this to use form fields directly
        context['form_fields'] = [
            (name, field) for name, field in form.fields.items()
        ]
        context['form'] = form
        return context


class UserUpdatePageView(UpdateView):
    model = DjangoUser
    template_name = 'update.html'
    success_url = reverse_lazy('users')
    form_class = UserUpdateForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            '''
            Unlike Flask with its url_for, Django's redirect
            internally calls reverse to resolve it, so there is no need for explicit reverse
            return redirect(reverse('users'))
            '''
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_fields'] = zip(self.get_form().fields.keys(), [field.label for field in self.get_form().fields.values()])
        context['field_name'] = 'username'
        return context
    
    def form_invalid(self, form):
        flash_messages = {
            'username_exists': 'Please use a different username',
        }
        if form.errors.get('username'):
            messages.error(self.request, flash_messages['username_exists'], extra_tags='warning')
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