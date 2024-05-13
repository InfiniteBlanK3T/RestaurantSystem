import json
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
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
@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = CustomUserCreationForm(data)
            if form.is_valid():
                user = form.save()
                return JsonResponse({'success': True, 'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({'success': False, 'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid request data'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@csrf_exempt
def user_login(request):
    if request.method == 'POST':# Decode the request body# Print the request body
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            print("Username:", username)  # Print the username
            print("Password:", password)  # Print the password
        except (ValueError, KeyError):
            return JsonResponse({'success': False, 'error': 'Invalid request data'}, status=400)

        user = authenticate(username=username, password=password)
        if user is not None:
            # Generate access and refresh tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            # Return the access token in the response
            return JsonResponse({'success': True, 'access': access_token}, status=200)
        else:
            return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=401)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
def user_logout(request):
    logout(request)
    return JsonResponse({'success': True, 'message': 'User logged out successfully'}, status=status.HTTP_200_OK)