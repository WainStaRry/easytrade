from rest_framework import viewsets, permissions
from .models import Message
from .serializers import MessageSerializer

# Viewset for messaging; users see messages they sent or received
class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(sender=user) | Message.objects.filter(receiver=user)
