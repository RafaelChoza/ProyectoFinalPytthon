from rest_framework import generics, permissions
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer, RegisterSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.models import User

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Solo el dueño puede editar el objeto, los demás solo leen.
    """

    def has_object_permission(self, request, view, obj):
        # Permite GET, HEAD o OPTIONS para todos
        if request.method in permissions.SAFE_METHODS:
            return True
        # Solo el owner puede modificar
        return obj.owner == request.user

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrReadOnly]

class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Un usuario solo ve sus propias órdenes
        return Order.objects.filter(user=self.request.user)
    
    def get_serializer_context(self):
        return {'request': self.request}

class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        obj = super().get_object()
        if self.request.method in permissions.SAFE_METHODS:
            return obj
        if self.request.user != obj:
            raise PermissionDenied("No puedes modificar a otros usuarios")
        return obj

class UsersListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class RegisterUserView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]