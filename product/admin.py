from django.contrib import admin
from .models import Product, Category, ProductProperty, Cart, Order
# Register your models here.



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image') 
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','category', 'rating', 'name', 'stock', 'description', 'image', 'actual_price', 'price', 'rating')
    list_editable = ('actual_price', 'price', 'stock')

 



@admin.register(ProductProperty)
class ProductPropertyAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'name', 'rating', 'stock', 'description', 'image', 'actual_price', 'price', 'rating') 
    list_editable = ('actual_price', 'price', 'stock')



@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_property', 'is_not_order') 


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_item', 'amount', 'date', 'is_receive_product')
    list_editable = ('is_receive_product', )
    
     



