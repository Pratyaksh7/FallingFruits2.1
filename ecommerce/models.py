from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Location(models.Model):
    state= models.CharField(max_length=60, null=True)
    city = models.CharField(max_length=60)
    latitude = models.DecimalField(max_digits=8,decimal_places=4)
    longitude = models.DecimalField(max_digits=8,decimal_places=4)
    farm = models.TextField()

    def __str__(self):
        return str(self.city+", "+self.state)



class Customer(models.Model):
    user =models.OneToOneField(User, on_delete=models.CASCADE, null=True,blank=True)
    name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name                

class Product(models.Model):
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    price = models.IntegerField()
    image = models.ImageField(upload_to="shop/images")     

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.customer.name  

    @property
    def total_cart_price(self):
        total = 0
        total_order_items = self.orderitem_set.all()
        for i in total_order_items:
            total += i.get_total
        return total

    @property
    def total_cart_fruits(self):
        total = 0
        total_order_items = self.orderitem_set.all()
        for i in total_order_items:
            total += i.quantity
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.product.name + ", "+ str(self.quantity) 

    @property
    def get_total(self):
        total = self.quantity * self.product.price
        return total

class Shipping(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=100,null=True)
    state = models.CharField(max_length=100,null=True)
    zipcode = models.CharField(max_length=100,null=True)
    
    def __str__(self):
        return self.address

