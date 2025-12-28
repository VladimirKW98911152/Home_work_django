from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import logout
from news.models import Author

class LoginView(AuthLoginView):
    template_name = 'sign/login.html'
    
    def get_success_url(self):
        return reverse_lazy('news_list')

class LogoutView(TemplateView):
    template_name = 'sign/logout.html'
    
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('news_list')

class SignUpView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'sign/signup.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        user = form.save()

        try:
            common_group = Group.objects.get(name='common')
            user.groups.add(common_group)
        except Group.DoesNotExist:

            common_group = Group.objects.create(name='common')
            user.groups.add(common_group)
        return super().form_valid(form)

class UpgradeView(TemplateView):
    template_name = 'sign/upgrade.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        user = request.user

        author, created = Author.objects.get_or_create(authorUser=user)
        if created:
            print(f"Создан Author для пользователя: {user.username}")


        try:
            authors_group = Group.objects.get(name='authors')
            user.groups.add(authors_group)
        except Group.DoesNotExist:
 
            authors_group = Group.objects.create(name='authors')
            user.groups.add(authors_group)

        return redirect('news_list')
