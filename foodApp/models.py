from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class RestaurantOwner(models.Model):
    name=models.CharField(max_length=100)
    surname=models.CharField(max_length=100)

    def __str__(self):
        return self.name + " " + self.surname
    
class CustomUser(AbstractUser):
    ROLE_CHOICES= (
        ('a', 'Admin'),
        ('r', 'Retailer'),
        ('c', 'Customer')
    )
    role=models.CharField(max_length=10, choices=ROLE_CHOICES, )

class Category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Food(models.Model):
    title=models.CharField(max_length=100)
    price=models.IntegerField()
    description=models.TextField()
    owner=models.ForeignKey(RestaurantOwner, on_delete=models.CASCADE)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    image=models.ImageField(upload_to="foods")

    def __str__(self):
        return self.title

class Cart(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    food=models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField(default=1)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "User: " + self.user.username + " Food: " + self.food.title

class DeliveryInfo(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    surname=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)

    def __str__(self):
        return "delivery info for " + self.user.username

class Order(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_price=models.IntegerField()
    delivery_info=models.ForeignKey(DeliveryInfo, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)



