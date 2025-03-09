from rest_framework import viewsets, permissions
from .models import Review
from .serializers import ReviewSerializer

# Viewset for product reviews
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Review.objects.all()
