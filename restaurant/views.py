import json
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.csrf import csrf_exempt


# Rest Framework
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.decorators.csrf import csrf_exempt


from .forms import CustomUserCreationForm
from .permissions import IsCustomer, IsRestaurantStaff
from .serializers import MenuItemSerializer, OrderSerializer, ReservationSerializer

from .models import MenuItem, Order, Reservation

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Include additional user information in the token payload
        user = self.user
        data['user_id'] = user.id
        data['user_role'] = user.role
        
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request):
        # Override the post method to include additional logic
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Perform additional checks or logic based on user role
            if user.role == 'staff':
                # Staff-specific logic
                # staff_permissions = ['view_orders', 'manage_inventory']
                # request.user.user_permissions.add(*staff_permissions)
                pass
            elif user.role == 'customer':
                # Customer-specific logic
                # request.user.default_payment_method = 'credit_card'
                pass
            
            # Call the parent's post method to generate and return the tokens
            return super().post(request)
        else:
            # Handle invalid credentials
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsRestaurantStaff]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer]

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer]

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    form = CustomUserCreationForm(request.data)
    if form.is_valid():
        user = form.save()
        return Response({'success': True, 'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'success': False, 'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)

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