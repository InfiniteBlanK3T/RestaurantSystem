from django.urls import path, include
from rest_framework import routers
from . import views
from .views import MenuItemViewSet, OrderViewSet, ReservationViewSet, CustomTokenObtainPairView, UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'menu-items', MenuItemViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'restaurants', views.RestaurantViewSet)
router.register(r'feedbacks', views.FeedbackViewSet)

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', include(router.urls)),
]