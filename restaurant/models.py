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
    phone_number=models.CharField(max_length=20, blank=True, null=True)
    address=models.CharField(max_length=255, blank=True, null=True)
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
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return super().__str__()

    @property
    def image(self):
        if self.image_upload:
            return self.image_upload.url
        elif self.image_url:
            return self.image_url
        else:
            return None

    
    # Add any additional fields

class Order(models.Model):
    STATUS_CHOICES = [
            ('received', 'Received'),
            ('preparing', 'Preparing'),
            ('ready', 'Ready'),
            ('delivered', 'Delivered'),
            ('cancelled', 'Cancelled'),
    ]
    AUS_STATES = [
        ('NSW', 'New South Wales'),
        ('VIC', 'Victoria'),
        ('QLD', 'Queensland'),
        ('SA', 'South Australia'),
        ('WA', 'Western Australia'),
        ('TAS', 'Tasmania'),
        ('NT', 'Northern Territory'),
        ('ACT', 'Australian Capital Territory'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, default='N/A')
    address = models.CharField(max_length=255, default='N/A')
    city = models.CharField(max_length=255, default='N/A')
    state_province = models.CharField(max_length=255, choices=AUS_STATES, default='VIC')
    zip_postal_code = models.CharField(max_length=10, default='N/A')
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Received')
    
    def __str__(self) -> str:
        return super().__str__()
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='menu_item_orders')
    quantity = models.PositiveIntegerField()
    
    def __str__(self) -> str:
        return super().__str__()
    
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    party_size = models.PositiveIntegerField()
    # Add any additional fields
    
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.PositiveIntegerField()
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)