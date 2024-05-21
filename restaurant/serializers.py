from rest_framework import serializers
from .models import MenuItem, Order, Reservation, Restaurant, OrderItem

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'image', 'restaurant']
        
class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())
      
    class Meta:
        model = OrderItem
        fields = ['menu_item', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['user', 'full_name', 'address', 'city', 'state_province', 'zip_postal_code', 'total_amount', 'status', 'order_items']

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        for order_item_data in order_items_data:
            print(f'order_item_data: {order_item_data}')  # Debug print
            menu_item_id = order_item_data.pop('menu_item').id
            quantity = order_item_data.pop('quantity')
            print(f'menu_item_id: {menu_item_id}, quantity: {quantity}')  # Debug print
            OrderItem.objects.create(order=order, menu_item_id=menu_item_id, quantity=quantity)
        return order

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'user', 'restaurant', 'date', 'time', 'party_size']
        
class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'