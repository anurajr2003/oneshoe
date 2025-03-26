from django.db import models
from django.contrib.auth.models import User  # Assuming you use Django's auth system
from datetime import datetime
import random




class Login(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)

class User(models.Model):
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE)
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    gender = models.CharField(max_length=20)
    isapprove = models.BooleanField(default=True)
    isdelete = models.BooleanField(default=False)

class Product(models.Model):
    productname = models.CharField(max_length=1000)
    brandname = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    colour = models.CharField(max_length=100)
    price = models.IntegerField()
    category = models.CharField(max_length=100)
    producttype = models.CharField(max_length=100)
    quantity = models.IntegerField(default=10)
    size = models.IntegerField(default=3)
    image = models.ImageField()

class Cart(models.Model):
    prd_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Login, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    cart_date = models.DateField(default=datetime.now)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

class Booking(models.Model):
    user_id = models.ForeignKey(Login, on_delete=models.CASCADE)
    totalprice = models.IntegerField(default=0)
    status = models.CharField(max_length=50, default='Packing')

class Bookingitem(models.Model):
    user_details = models.ForeignKey(User, on_delete=models.CASCADE)
    product_details = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    payment_amount = models.IntegerField()
    payment_status = models.CharField(max_length=255, default='pending')
    order_status = models.CharField(max_length=255, default='ordered')
    created_at = models.DateTimeField()



class BookingAddress(models.Model):
    userdetails=models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.IntegerField(default=0)
    state = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.IntegerField(default=0)
    total_amount = models.IntegerField(default=0)
    status = models.CharField(max_length=50, default='Packing')

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')  # Prevents duplicate wishlist entries

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_id = models.CharField(max_length=100, unique=True)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, default="Pending")

    def __str__(self):
        return f"Order {self.order_id} - {self.status}"

class UserCarts(models.Model):
    user_details = models.ForeignKey(User, on_delete=models.CASCADE)
    product_details = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

class ProductsOrders(models.Model):
    user_details = models.ForeignKey(Login, on_delete=models.CASCADE)
    product_details = models.ForeignKey(Product, on_delete=models.CASCADE)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    payment_status = models.CharField(max_length=20, default="Pending")
    product_code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(default=datetime.now)


class PasswordReset(models.Model):
    User = models.ForeignKey(User,on_delete=models.CASCADE)
    token = models.CharField(max_length=255)



