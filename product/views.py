from django.shortcuts import render
from product.models import Product, ProductProperty, Cart,Order, Category 
from user.models import User
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages



@login_required(login_url='sign_in')
def dashboard(request):
     context = { 'title' : "Dashboard",
                'products': Product.objects.all(),
                'feature_product' : Product.objects.filter().order_by()[:4],
                'category_products': Category.objects.all(),
                }   
     return render(request, 'product/dashboard.html', context=context)


@login_required(login_url='sign_in')
def show_product(request, id=None):
     stock = Product.objects.get(id=id).stock
     if id is not None and stock > 0 : 
          context = { 'title' : "Show Product",
                    'show_products_property': ProductProperty.objects.filter(product_name__id=id),
                    'show_product_id':id 
                    }
          return render(request, 'product/show_product.html', context=context)   
     messages.error(request, 'OUT OF STOCK !!')      
     return  HttpResponseRedirect(reverse('dashboard'))     


@login_required(login_url='sign_in')
def add_cart(request, id=None, show_product_id=None):
     if id is not None: 
          product_property_instance = ProductProperty.objects.get(id=id)
          # product_instance = product_property_instance.product_name 
          user_instance = User.objects.get(email=request.user)
          # user = Cart(user=user_instance, product_property=product_property_instance)
          # user.save()
          response = HttpResponseRedirect(reverse('show_product', kwargs={"id": show_product_id}))
          value = request.COOKIES.get(str(id))
          if value is None: 
               response.set_cookie(str(id) , product_property_instance.stock-1)
          else: 
               if int(value) == 0:
                    messages.error(request, 'OUT OF STOCK !!') 
                    return  HttpResponseRedirect(reverse('dashboard'))     
               response.set_cookie(str(id) ,int(value)-1)     
          user = Cart(user=user_instance, product_property=product_property_instance)
          user.save()
          
          return response 
   

@login_required(login_url='sign_in')
def show_cart(request):
     user_instance = User.objects.get(email=request.user)
     cart_queryset = Cart.objects.filter(user=user_instance, is_not_order=True)
     total_price = 0 
     for instance in cart_queryset:
          total_price += instance.product_property.price 
     context = { 'title' : "Show Cart", 
                 'cart_queryset' : cart_queryset,
                 'total_price': total_price
               }
     return render(request, 'product/show_cart.html', context=context)



@login_required(login_url='sign_in')
def remove_item(request, id=None):
     if id is not None:
          remove_data = Cart.objects.get(id=id)
          remove_data.delete()
          value = request.COOKIES.get(str(id))
          if value is not None: 
               response = HttpResponseRedirect(reverse('show_cart'))
               response.set_cookie(str(id) , int(value)+1)
          
               return response 
          return HttpResponseRedirect(reverse('show_cart'))  


@login_required(login_url='sign_in')
def order_item(request, amount=None):
     if amount is not None:
          user_instance = User.objects.get(email=request.user)
          cart_queryset = Cart.objects.filter(user=user_instance)
          for instance in cart_queryset:
               if instance.is_not_order:
                    product_property = instance.product_property 
                    product_property.stock -= 1 
                    product_property.save() 
                    product = instance.product_property.product_name
                    product.stock -= 1
                    product.save()
                    order_item = Order(user=user_instance, order_item=instance, amount=amount)
                    order_item.save()
                    instance.is_not_order = False 
                    instance.save() 
          messages.success(request, ' Successfully Order items  !!! !!')           
          return  HttpResponseRedirect(reverse('show_order_item'))
          
@login_required(login_url='sign_in')         
def show_order_item(request):
     user_instance = User.objects.get(email=request.user)
     order_item_queryset = Order.objects.filter(user=user_instance, is_receive_product=False)
     context = { 'title' : 'Order Item',
                'order_item_queryset': order_item_queryset, 
               }
     return render(request, 'product/show_order_item.html', context=context)

               
@login_required(login_url='sign_in')
def cancel_product(request, id=None):
     if id is not None:
          order_cancel = Order.objects.get(id=id)
          product_property = order_cancel.order_item.product_property
          product_property.stock += 1 
          product_property.save() 
          product = order_cancel.order_item.product_property.product_name
          product.stock += 1 
          product.save() 
          order_cancel.delete()

          return  HttpResponseRedirect(reverse('show_order_item'))

@login_required(login_url='sign_in')
def user_order_history(request):
    user_instance = User.objects.get(email=request.user)
    order_items_queryset = user_instance.order.filter(is_receive_product=True)
    context = { 'title' : 'Order History',
                'order_items_queryset' : order_items_queryset
    }
    return render(request, 'product/user_order_history.html', context=context)
