from rest_framework import viewsets, permissions
from .models import CartItem
from .serializers import CartItemSerializer

# Viewset for Cart Items for the logged-in user
class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)
