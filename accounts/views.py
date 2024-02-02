from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.contrib.auth.models import User, Group
from django.views.generic import CreateView, UpdateView

from accounts.forms import LoginForm, RegisterForm, GroupPermissionAddForm


# Create your views here.
class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next = request.GET.get('next', 'home')
                return redirect(next)
        return render(request, 'login.html', {'form': form})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('home')


class RegistrationView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'registration.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            login(request, user)
            return redirect('home')
        return render(request, 'registration.html', {'form': form})

class HomeView(View):
    def get(self, request):

        return render(request, 'index.html', )


