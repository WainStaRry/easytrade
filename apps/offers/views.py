from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Offer
from .serializers import OfferSerializer

@login_required
def make_offer(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'make_offer.html', {'product': product})

@login_required
def offers_received(request):
    offers = Offer.objects.filter(product__seller=request.user).order_by('-created_at')
    return render(request, 'offer_list.html', {
        'offers': offers,
        'view': 'received'
    })

@login_required
def offers_sent(request):
    offers = Offer.objects.filter(buyer=request.user).order_by('-created_at')
    return render(request, 'offer_list.html', {
        'offers': offers,
        'view': 'sent'
    })

class OfferViewSet(viewsets.ModelViewSet):
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Offer.objects.filter(
            models.Q(buyer=user) | models.Q(product__seller=user)
        )

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        offer = self.get_object()
        if request.user != offer.product.seller:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        if offer.offer_status != 'pending':
            return Response({'error': 'Offer cannot be accepted'}, status=status.HTTP_400_BAD_REQUEST)
        
        offer.offer_status = 'accepted'
        offer.save()
        
        # 可以在这里添加创建订单的逻辑
        
        return Response({'message': 'Offer accepted successfully'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        offer = self.get_object()
        if request.user != offer.product.seller:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        if offer.offer_status != 'pending':
            return Response({'error': 'Offer cannot be rejected'}, status=status.HTTP_400_BAD_REQUEST)
        
        offer.offer_status = 'rejected'
        offer.save()
        return Response({'message': 'Offer rejected successfully'})
