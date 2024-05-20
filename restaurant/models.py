from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    USER_ROLES = (
        ('customer', 'Customer'),
        ('staff', 'Restaurant Staff'),
        ('admin', 'Admin'),
    )
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='customer')
    
class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    # Add any additional fields
    
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_upload = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    image_url = models.URLField(max_length=200, blank=True, null=True)

    @property
    def image(self):
        if self.image_upload:
            return self.image_upload.url
        elif self.image_url:
            return self.image_url
        else:
            return None
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    
    # Add any additional fields

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20)
    # Add any additional fields
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    party_size = models.PositiveIntegerField()
    # Add any additional fields
    
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)