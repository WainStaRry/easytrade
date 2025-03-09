from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Offer
from .serializers import OfferSerializer

# Viewset for handling offers and seller responses
class OfferViewSet(viewsets.ModelViewSet):
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Offer.objects.all()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def accept(self, request, pk=None):
        offer = self.get_object()
        if request.user == offer.product.seller:
            offer.offer_status = 'accepted'
            offer.save()
            return Response({'message': 'Offer accepted'})
        return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def reject(self, request, pk=None):
        offer = self.get_object()
        if request.user == offer.product.seller:
            offer.offer_status = 'rejected'
            offer.save()
            return Response({'message': 'Offer rejected'})
        return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
