from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Product
from .serializers import ProductSerializer
from .forms import ProductForm
from django.contrib.auth.decorators import login_required



# REST API viewset for Product CRUD operations
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category', 'seller']
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']

# View for posting a new product via a web form
class PostProductView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'
    
    def get(self, request):
        form = ProductForm()
        return render(request, 'post_product.html', {'form': form})
    
    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('home')
        return render(request, 'post_product.html', {'form': form})

@login_required
def my_products_view(request):
    user_products = Product.objects.filter(seller=request.user)
    return render(request, "my_products.html", {"user_products": user_products})
