from django.db import models
import datetime
from user.models import User 
from django.core.exceptions import ValidationError
# Create your models here.


def rating_validation(value):
    if value > 6 and value == 0 :
        raise ValidationError(
            _('%(value)s should be less than 6 and greater than 0'),
            params={'value': value},
        )

class Category(models.Model):
    name = models.CharField(max_length=40)
    image = models.ImageField(upload_to="images/product/" + str(datetime.datetime.now()) + "/" )

    
    def __str__(self):
        return self.name 
  
  
  
class ProductAbstract(models.Model):
    name = models.CharField(max_length=50) 
    stock = models.IntegerField()
    description = models.CharField(max_length=50)
    image = models.ImageField(upload_to="images/product/" + str(datetime.datetime.now()) + "/" )
    price = models.IntegerField()
    rating = models.IntegerField(null=True, blank=True, validators=[rating_validation])
    actual_price = models.IntegerField(null=True)  
    
    class Meta:
        abstract = True    
    
class Product(ProductAbstract):
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    
    # name = models.CharField(max_length=50) 
    # stock = models.IntegerField()
    # description = models.CharField(max_length=50)
    # image = models.ImageField(upload_to="images/product/" + str(datetime.datetime.now()) + "/" )
    # price = models.IntegerField()
    
    def __str__(self):
        return self.name 
    
class ProductProperty(ProductAbstract): 
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE, )   
    color = models.CharField(max_length=50, null=True)
    # image = models.ImageField(upload_to="images/product/" + str(datetime.datetime.now()) + "/" )
    
    
    
    def __str__(self):
        return self.product_name.name
    
    
class Cart(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    # product_name = models.ForeignKey(Product, on_delete=models.CASCADE, )   
    product_property =  models.ForeignKey(ProductProperty, on_delete=models.CASCADE, )
    is_not_order = models.BooleanField(default=True)
  
    
    def __str__(self):
        return self.product_property.product_name.name
    
     
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order")  
    order_item = models.ForeignKey(Cart, on_delete=models.CASCADE) 
    amount = models.IntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True) 
    is_receive_product = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email
