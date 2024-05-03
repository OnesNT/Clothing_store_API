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
    return HttpResponse("Hello world")



