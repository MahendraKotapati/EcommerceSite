"""ShoppingCart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shopping.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='index'),
    path('index/',index,name='index'),
    path('update_item/',update_item_quantity,name='update_item_quantity'),
    path('confirm_order/',confirm_order,name='confirm_order'),
    path('remove_item/',remove_item,name='remove_item'),
    path('thankyou/',thank_you,name='thank_you'),
    path('cart/',cart,name='cart'),
    path('credit_card_page/',credit_card_page,name='credit_card_page'),
    path('add_to_cart/',add_to_cart,name='add_to_cart'),


]
