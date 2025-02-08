from django.shortcuts import reverse, redirect
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from task_manager.users.models import User
from django.contrib.auth.models import User as DjangoUser
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login

# Create your views here.

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
    template_name = 'index_users.html'
    model = User
    context_object_name = 'users'

    def get_queryset(self):
        return DjangoUser.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields_names'] = ['ID', 'Username']
        return context

class UserCreatePageView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'create.html'
    success_url = reverse_lazy('users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form()
        context['form_fields'] = zip(form.fields.keys(), [field.label for field in form.fields.values()])
        return context
    
    # Automatic login after successful registration
    def form_valid(self, form):
        user = form.save()
        try:
            login(self.request, user)
            return redirect(self.get_success_url())
        # AttributeError is raised when the form is invalid
        except AttributeError:
            return self.form_invalid(form)

    def form_invalid(self, form):
        flash_messages = {
            'username_exists': 'Please use a different username',
            'password1': 'Please enter your password',
            'password2': 'Please use stronger passwords that match',
        }
        if form.errors.get('username'):
            messages.error(self.request, flash_messages['username_exists'], extra_tags='warning')
        if form.errors.get('password1'):
            messages.error(self.request, flash_messages['password1'], extra_tags='warning')
        if form.errors.get('password2'):
            messages.error(self.request, flash_messages['password2'], extra_tags='warning')
        if form.non_field_errors():
            messages.error(self.request, form.non_field_errors(), extra_tags='warning')
        return super().form_invalid(form)

class UserUpdatePageView(UpdateView):
    model = User
    template_name = 'update.html'
    success_url = reverse_lazy('users')

class UserDeletePageView(DeleteView):
    model = User
    template_name = 'delete.html'
    success_url = reverse_lazy('users')