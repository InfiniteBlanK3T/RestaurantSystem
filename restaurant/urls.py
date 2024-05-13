from django.urls import path, include
from rest_framework import routers
from . import views
from .views import MenuItemViewSet, OrderViewSet, ReservationViewSet

router = routers.DefaultRouter()
router.register(r'menu-items', MenuItemViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'reservations', ReservationViewSet)

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', include(router.urls)),
]