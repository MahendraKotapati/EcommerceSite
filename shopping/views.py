from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import View
from shopping.models import Product,Item,Cart
import string
import random

def index(request):
    user=request.user
    items=''
    if user.is_anonymous:
        user=''
    else :
        items=Item.objects.filter(cart__user=user, cart__checked_out=False)
        items=items.count() if items else 0
    products= Product.objects.filter(total_items__gt=0)

    return render(request,'index.html',{'products':products,'user':user,'items':items,'page':'home'})

def add_to_cart(request):
    user=request.user
    if user.is_anonymous:
        chars = string.ascii_uppercase+string.ascii_letters
        user_name = ' '.join( random.choice(chars) for _ in range(9) )
        password = '1234567p'
        user = User.objects.create(username=user_name,first_name='guest',last_name='guest',email='guest@gmail.com',is_active=True,is_staff=True)
        user.set_password(password)
        user.save()
        user = authenticate(username=user_name, password=password)

        if user:
            login(request,user)

    product_id = request.GET.get('product_id')
    cart = Cart.objects.filter(checked_out=False,user=user)
    cart = cart[0]  if cart else ''
    if not cart:
        cart = Cart.objects.create(user=user)
    Item.objects.create(cart=cart,product_id=product_id,quantity=1)
    return redirect('index')
    


def calculate_sum(cart_items):
    items_sum=0
    for item in cart_items:
        items_sum = items_sum + (item.quantity*item.product.unit_price)
    
    return items_sum


def cart(request):
    user = request.user
    items = ''
    cart_items = []
    if user.is_anonymous:
        user = ''
    else:
        cart_items = Item.objects.filter(cart__user = user, cart__checked_out=False)
        items = cart_items.count() if cart_items else  0
    items_sum = calculate_sum(cart_items)
    return render(request,'cart.html',{'user':user,'items':items,'page':'cart','cart_items':cart_items,'sum':items_sum})


def update_item_quantity(request):
    item_id = request.GET.get('item_id')
    quantity = request.GET.get('quantity')
    item = Item.objects.get(id=item_id)
    if(item.product.total_items>=int(quantity)):
        item.quantity = quantity
        item.save()
    
    return redirect('cart')

def thank_you(request):
    user = request.user
    items = ''
    cart_items = []
    if user.is_anonymous:
        user = ''
    else:
        cart_items = Item.objects.filter(cart__user=user,cart__checked_out=False)
        items = cart_items.count() if cart_items else 0
    
    items_sum =calculate_sum(cart_items)

    return render(request,'thankyou.html',{'user':user,'items':items,'page':'cart','cart_items':cart_items,'sum':items_sum,'shopping':'continueShopping'})

         

def remove_item(request):
    item_id = request.GET.get('item_id')
    Item.objects.get(id=item_id).delete()
    return redirect('cart')


def confirm_order(request):
    user = request.user
    cart_items = Item.objects.filter(cart__user=user,cart__checked_out=False)
    items_sum = calculate_sum(cart_items)
    cart = Cart.objects.get(user=user,checked_out=False)
    cart.checked_out=True
    cart.save()
    User.objects.filter(username=user.username).delete()
    return render(request,'confirmorder.html',{'user':user,'items':0,'page':'cart','cart_items':cart_items,'items_sum':items_sum,'shopping':'ContinueShopping'})
    #return render(request,'confirmorder.html',{'user':request.user})

def credit_card_page(request):
    return render(request,'credit_card.html',{})
    
