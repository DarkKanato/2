from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Client, Product, Order
from .forms import ClientForm, ProductForm, OrderForm

def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ClientForm()
    return render(request, 'add_client.html', {'form': form})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

def add_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = OrderForm()
    return render(request, 'add_order.html', {'form': form})

def home(request):
    clients = Client.objects.all()  # Получаем всех клиентов из базы данных
    products = Product.objects.all()  # Получаем все товары
    orders = Order.objects.all()  # Получаем все заказы
    context = {
        'clients': clients,
        'products': products,
        'orders': orders,
    }
    return render(request, 'home.html', context)