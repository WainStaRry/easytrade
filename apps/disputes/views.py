from rest_framework import viewsets, permissions
from .models import Dispute
from .serializers import DisputeSerializer

# Viewset for handling disputes; admins see all, others see their own.
class DisputeViewSet(viewsets.ModelViewSet):
    serializer_class = DisputeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Dispute.objects.all()
        return Dispute.objects.filter(complainant=user)
