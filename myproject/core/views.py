from django.shortcuts import render
from django.http import HttpResponse
from core.models import Product
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, LoginForm
from .forms import ProductSearchForm

from rest_framework import generics # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
# from core.models import Product, Order


def index(request):
    return render(request, 'core/index.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('core:home')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('core:home')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})


