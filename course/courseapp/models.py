from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    image = models.ImageField(upload_to="product/")
    
class Fcourse(Product):
    author = models.CharField(max_length=100)
    # Other book-specific fields

class Cat1(Product):
    author = models.CharField(max_length=100)

    # Other electronics-specific fields

class Cat2(Product):
    author = models.CharField(max_length=100)
    # Other clothing-specific fields

class Cat3(Product):
    author = models.CharField(max_length=100)
    # Other clothing-specific fields

class Register(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    phone = models.IntegerField()
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    status = models.IntegerField(default=1)

# class Login(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.CharField(max_length=200)
#     password = models.CharField(max_length=100)

class CartItem(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)  # Add this line
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    # Add more fields as needed, such as user reference for tracking cart items per user

class Order(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)  # Add this line
    products = models.ManyToManyField(Product, through='OrderedItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderedItem(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)  # Add this line
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # quantity = models.PositiveIntegerField(default=1)
