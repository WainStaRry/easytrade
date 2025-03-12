<<<<<<< HEAD
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Review
from .serializers import ReviewSerializer
from apps.products.models import Product

=======
from rest_framework import viewsets, permissions
from .models import Review
from .serializers import ReviewSerializer

# Viewset for product reviews
>>>>>>> 1f1ec4b928cddfc092349168b2cf9870c33751a0
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Review.objects.all()
<<<<<<< HEAD

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

@login_required
def create_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'review_form.html', {'product': product})

def product_reviews(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product).order_by('-created_at')
    return render(request, 'review_list.html', {
        'product': product,
        'reviews': reviews
    })

from django.shortcuts import render
from .models import Review
from apps.products.models import Product

def review_home(request):
    # 获取所有有评价的产品
    products_with_reviews = Product.objects.filter(reviews__isnull=False).distinct()
    # 获取最新评价
    latest_reviews = Review.objects.select_related('product', 'reviewer').order_by('-created_at')[:10]
    
    context = {
        'products': products_with_reviews,
        'reviews': latest_reviews,
        'is_home': True
    }
    return render(request, 'review_list.html', context)
=======
>>>>>>> 1f1ec4b928cddfc092349168b2cf9870c33751a0
