from django.shortcuts import render
from django.http import HttpResponse
from core.models import Product
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, LoginForm
from .forms import ProductSearchForm

from rest_framework import generics # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from core.models import Product, Order
# from core.serializers import ProductSerializer, OrderSerializer

def index(request):
    return render(request, 'core/index.html')

# def home(request):
#     products = Products.objects.all()
#     return render(request, 'core/home.html', {'products': products})

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


def home(request):
    form = ProductSearchForm(request.GET)
    products = Product.objects.all()

    if 'query' in request.GET:
        query = request.GET['query']
        products = products.filter(name__icontains=query)

    return render(request, 'core/home.html', {'form': form, 'products': products})

def contact(request):
    return render(request,'core/contact.html')


# def product_list(request):
#     products = Products.objects.all()
#     return render(request, 'core/product_list.html', {'products': products})

# def product_detail(request, pk):
#     product = Products.objects.get(pk=pk)
#     return render(request, 'core/product_detail.html', {'product': product})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'cart/index.html', {'products': products})

# class ProductListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

# class OrderListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)