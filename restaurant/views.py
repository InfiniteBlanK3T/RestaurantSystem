# Rest Framework
from django.contrib.auth import authenticate
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated

from decimal import Decimal
from django.db.models import Count, Sum
from django.views.decorators.csrf import csrf_exempt


from .forms import CustomUserCreationForm
from .permissions import IsCustomer, IsRestaurantStaff
from .serializers import MenuItemSerializer, OrderSerializer, ReservationSerializer, RestaurantSerializer, FeedbackSerializer, UserSerializer

from .models import MenuItem, Order, Reservation, Restaurant, OrderItem, Feedback, User


class SalesAnalyticsView(APIView):
    permission_classes = [IsAuthenticated, IsRestaurantStaff]

    def get(self, request):
        # Total Revenue
        total_revenue = Order.objects.aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')

        # Average Order Value
        order_count = Order.objects.count()
        average_order_value = total_revenue / order_count if order_count > 0 else Decimal('0.00')

        # Popular Menu Items
        popular_menu_items = (
            OrderItem.objects.values('menu_item__name', 'menu_item__description', 'menu_item__price')
            .annotate(count=Count('menu_item'))
            .order_by('-count')[:10]
        )

        return Response({
            'total_revenue': total_revenue,
            'average_order_value': average_order_value,
            'popular_menu_items': list(popular_menu_items)
        })

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_queryset(self):
        user = self.request.user
        if IsRestaurantStaff().has_permission(self.request, self):
            return User.objects.all()
        else:
            return User.objects.filter(id=user.id)

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        return [permissions.IsAuthenticated(), IsRestaurantStaff()]

    def get_queryset(self):
        queryset = MenuItem.objects.all()
        restaurant_name = self.request.query_params.get('restaurant_name', None)
        if restaurant_name is not None:
            queryset = queryset.filter(restaurant__name=restaurant_name)
        return queryset

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        return [permissions.IsAuthenticated(), IsRestaurantStaff()]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        # Allow staff to view orders, but only allow customers to create, update, or delete orders
        if self.request.method in ['GET']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsCustomer()]
    
    def get_queryset(self):
        queryset = Order.objects.all()
        user = self.request.user
        if user.role == 'customer':
            queryset = queryset.filter(user=user)
        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id
        order_items_data = data.pop('order_items', [])
        order_serializer = self.get_serializer(data=data)
        if order_serializer.is_valid():
            order = order_serializer.save()
            for order_item_data in order_items_data:
                menu_item = MenuItem.objects.get(id=order_item_data.pop('menu_item'))
                OrderItem.objects.create(order=order, menu_item=menu_item, **order_item_data)
            return Response({'order_id': order.id}, status=status.HTTP_201_CREATED)
        print(f"Serializer errors: {order_serializer.errors}")
        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    form = CustomUserCreationForm(request.data)
    if form.is_valid():
        try:
            user = form.save()
            return Response({'success': True, 'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'success': False, 'message': 'Registration failed', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'success': False, 'message': 'Registration failed. Form is invalid', 'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        # Generate access and refresh tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            'success': True, 
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_200_OK)
    else:
        return Response({'success': False, 'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)

        return Response({'success': True, 'message': 'User logged out successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'success': False, 'message': 'Something went wrong', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)