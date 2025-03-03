from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import \
    ListView, CreateView, UpdateView, DeleteView


class BaseListView(ListView):
    context_object_name = 'table_content'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(getattr(self, 'context_extra', {}))
        return context


class BaseCreateView(CreateView):
    template_name = 'create.html'
    
    def form_valid(self, form):
        message_ = self.messages_show.get('success','')
        messages.success(
            self.request,
            f'{message_}: {form.instance.name}',
            extra_tags='.alert',
        )
        return super().form_valid(form)
    
    def form_invalid(self, form):
        message_ = self.messages_show.get('error','')
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    self.request,
                    f'{message_}: {field}: {error}',
                    extra_tags='.alert',
                )
        return redirect(self.success_url)


class BaseUpdateView(UpdateView):
    template_name = 'update.html'
    
    def form_valid(self, form):
        messages.success(
            self.request,
            self.messages_show.get(
                'success',
                'BaseUpdateView success'
            ),
            extra_tags='.alert',
        )
        return super().form_valid(form)


class BaseDeleteView(DeleteView):
    template_name = 'delete.html'
    
    def has_related_objects(self):
        # Метод переписывается в дочерних классах
        return False
        
    def post(self, request, *args, **kwargs):        
        if self.has_related_objects():
            messages.error(
                self.request,
                self.messages_show.get(
                    'error',
                    'BaseDeleteView error'
                ),
                extra_tags='.alert',
            )
            return redirect(self.success_url)
        
        response = super().post(request, *args, **kwargs)
        messages.success(
            self.request,
            self.messages_show.get(
                'success',
                'BaseDeleteView success'
            ),
            extra_tags='.alert',
        )
        return response
