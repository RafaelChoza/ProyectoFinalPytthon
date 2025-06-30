from django.urls import path
from .views import (
    ProductListCreateView,
    ProductRetrieveUpdateDestroyView,
    OrderListCreateView,
    RegisterUserView,
    UserRetrieveUpdateDestroyView,
    UsersListView,
    OrderListView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path("orders/all/", OrderListView.as_view(), name="orders"),
    path('register/', RegisterUserView.as_view(), name='user-register'),
    path("users/", UsersListView.as_view(), name="users"),
    path("users/<int:pk>", UserRetrieveUpdateDestroyView.as_view(), name="user-detail"),

    # JWT Auth endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # login - obtiene token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # refrescar token
]
