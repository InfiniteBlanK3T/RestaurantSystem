from rest_framework import serializers
from .models import MenuItem, Order, Reservation, Restaurant, OrderItem, Feedback, User

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'image_url', 'restaurant']
        
class OrderItemSerializer(serializers.ModelSerializer):      
    class Meta:
        model = OrderItem
        fields = ['id','menu_item', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['user', 'full_name', 'address', 'city', 'state_province', 'zip_postal_code', 'total_amount', 'status','created_at', 'order_items']

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items', [])
        order = Order.objects.create(**validated_data)
        for order_item_data in order_items_data:
            menu_item_id = order_item_data.pop('menu_item')
            quantity = order_item_data.pop('quantity')
            OrderItem.objects.create(order=order, menu_item_id=menu_item_id, quantity=quantity)
        return order

class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Reservation
        fields = ['id','user','restaurant', 'date', 'time', 'party_size']
        
class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(readonly=True) // test
    
    class Meta:
        model = Feedback
        fields = [ 'order', 'rating', 'comment', 'created_at']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'address', 'role']