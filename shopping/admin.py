from django.contrib import admin
from shopping.models import Product, Item, Cart
# Register your models here.

class ItemAdmin(admin.ModelAdmin):
    class Meta:
        model = Item
    
    list_display = (
        'product_title','product_price','cart','quantity'
    )

    def product_title(self,obj):
        return obj.product.title
    
    def product_price(self,obj):
        return obj.product.unit_price

admin.site.register(Product)
admin.site.register(Item,ItemAdmin)
admin.site.register(Cart)