from django.contrib import admin
from .models import User, Restaurant, MenuItem, Order, OrderItem, Reservation, Feedback

models = [User, Restaurant, MenuItem, Order, OrderItem, Reservation, Feedback]

for model in models:
    admin.site.register(model)