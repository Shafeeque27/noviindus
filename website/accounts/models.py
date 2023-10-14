from django.db import models

# Create your models here.


class CustomUser(models.Model):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Cart(models.Model):
    user = models.CharField(max_length=100)
    product = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
