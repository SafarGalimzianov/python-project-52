from django.shortcuts import reverse, redirect
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from task_manager.users.models import User
from django.contrib.auth.models import User as DjangoUser
from task_manager.users.forms import UserUpdateForm
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

    # I should use models fields instead of hardcoding them
    # Pass them to template and make template refer to them in variables
    # Like user.field1 etc
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
        context['form_fields'] = zip(self.get_form().fields.keys(), [field.label for field in self.get_form().fields.values()])
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