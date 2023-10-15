from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from .forms import RegistrationForm, LoginForm
from .models import CustomUser, Product, Cart
from .models import *
from django.http import HttpResponseRedirect

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid() and form.cleaned_data['password'] == form.cleaned_data['confirm_password']:
            user = CustomUser(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=make_password(form.cleaned_data['password'])
            )
            user.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/registration.html', {'form':form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
           return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def home(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'accounts/home.html', context)

def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'accounts/cart.html', {'cart_items': cart_items})

def add_to_cart(request, product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, pk=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product_name=product.name)
    if not created:
        cart_item.quantity += 1
        cart_item.price = Product.price
        cart_item.save()
    return HttpResponseRedirect('/cart/')

def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    cart_item.delete()
    return HttpResponseRedirect('/cart/')