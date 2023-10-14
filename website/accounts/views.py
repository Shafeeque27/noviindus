from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .forms import RegistrationForm, LoginForm
from .models import CustomUser, Product, Cart
from .models import *

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
    user = CustomUser.objects.get(username=request.session['username'])
    cart_items = Cart.objects.filter(user=user)
    total_quantity = 0
    for item in cart_items:
        total_quantity += item.quantity
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_quantity': total_quantity})

def add_to_cart(request, product_id):
    user = CustomUser.objects.get(username=request.session['username'])
    product = Product.objects.get(pk=product_id)
    Cart.objects.create(user=user, product=product)
    return redirect('cart')

def delete_from_cart(request, cart_id):
    cart_item = Cart.objects.get(pk=cart_id)
    user = CustomUser.objects.get(username=request.session['username'])
    if cart_item.user == user:
        quantity = cart_item.quantity
        cart_item.delete()
        return redirect('cart')
    else:
        return redirect('cart')