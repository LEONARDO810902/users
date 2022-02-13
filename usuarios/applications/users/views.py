from .models import User
import datetime

from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

# Create your views here.

from django.views.generic import (
    View,
    CreateView,
)

from django.views.generic.edit import (
    FormView,
)

from .forms import (
    UserCreateForm,
    LoginForm,
    UpdatePasswordForm,
)


class FechaMixin(object):
    def get_context_data(self, **kwargs):
        context = super(FechaMixin, self).get_context_data(**kwargs)
        context['fecha'] = datetime.datetime.now()
        return context


class UserCreateView(FechaMixin, FormView):
    template_name = 'users/create.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('home_app:home-panel')

    def form_valid(self, form):
        #
        User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['password1'],
            form.cleaned_data['email'],
            nombres=form.cleaned_data['nombres'],
            apellidos=form.cleaned_data['apellidos'],
            genero=form.cleaned_data['genero'],
        )
        #
        return super(UserCreateView, self).form_valid(form)


class LoginUsers(FechaMixin, FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:home-panel')

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        login(self.request, user)
        return super(LoginUsers, self).form_valid(form)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'users_app:user-login'
            )
        )


class UpdatePasswordView(LoginRequiredMixin, FechaMixin, FormView):
    template_name = 'users/UpdateLogin.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:user-login')
    login_url = reverse_lazy('users_app:user-login')

    def form_valid(self, form):
        usuario = self.request.user
        user = authenticate(
            username=usuario.username,
            password=form.cleaned_data['password1']
        )
        if user:
            new_password = form.cleaned_data['password2']
            usuario.set_password(new_password)
            usuario.save()
            logout(self.request)
        return super(UpdatePasswordView, self).form_valid(form)
