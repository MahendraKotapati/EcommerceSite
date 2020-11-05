from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import View
from shopping.models import Product,Item,Cart
import string
import random



def index(request):
    user=request.user
    items=''
    cart_items_count = 0
    if user.is_anonymous:
        user=''
    else :
        items=Item.objects.filter(cart__user=user, cart__checked_out=False)
        #items=items.count() if items else 0
        cart_items_count = 0
        for i in items:
            cart_items_count+= i.quantity
    products= Product.objects.filter(total_items__gt=0)

    return render(request,'index.html',{'products':products,'user':user,'items':cart_items_count,'page':'home'})

@login_required(login_url='/login')
def add_to_cart(request):
    user=request.user
    
    product_id = request.GET.get('product_id')
    cart = Cart.objects.filter(checked_out=False,user=user)
    cart = cart[0]  if cart else ''
    if not cart:
        cart = Cart.objects.create(user=user)
    
    try:
        quantity = Item.objects.get(cart=cart,product_id=product_id).quantity
        item = Item.objects.get(cart=cart,product_id=product_id)

        if(item.product.total_items>=quantity+1):
            item.quantity = quantity+1
            item.save()
        else:
            messages.error(request,'currently we dont have '+ str(quantity+1) + ' items for this product')
    except:
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
        #items = cart_items.count() if cart_items else  0
        items = 0
        for i in cart_items:
            items+= i.quantity
    items_sum = calculate_sum(cart_items)
    return render(request,'cart.html',{'user':user,'items':items,'page':'cart','cart_items':cart_items,'sum':items_sum})


def update_item_quantity(request):
    item_id = request.GET.get('item_id')
    quantity = request.GET.get('quantity')
    item = Item.objects.get(id=item_id)
    
    try:
        if(item.product.total_items>=int(quantity)):
            item.quantity = quantity
            item.save()
        else:
            messages.error(request,'currently we dont have '+ quantity + ' items for this product')
           
    except Exception as e:
        messages.error(request,' Please enter Positive Number as Quantity')
     
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
    #User.objects.filter(username=user.username).delete()
    return render(request,'confirmorder.html',{'user':user,'items':0,'page':'cart','cart_items':cart_items,'items_sum':items_sum,'shopping':'ContinueShopping'})

def credit_card_page(request):
    return render(request,'credit_card.html',{})
    

def sign_up(request):

    if request.method=='POST': 
        #username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        email= request.POST.get('email', '')
        try:
            if(User.objects.get(email=email)):
                messages.success(request,'you already have an account please login')
                return redirect('login')
        except:
            pass
                
        user = User.objects.create_user(username=email, password=password,email=email) 
        #messages.success(request,'Your have SignedUp successfully .')
        login(request,user,backend='django.contrib.auth.backends.ModelBackend')
         
        return redirect('index')

    return render(request,'signup.html')


def login_view(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user  =  authenticate(username=username,password= password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else: 
            messages.error(request,'please check username and password')
            return redirect('login')
    else:
        return render(request,'login.html')

    
def logout_view(request):
    logout(request)

    system_messages = messages.get_messages(request)
    for message in system_messages:
        pass

    messages.success(request,'successfully logged out')
    return redirect('login')