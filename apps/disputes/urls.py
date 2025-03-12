from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'api/disputes', views.DisputeViewSet, basename='dispute')

urlpatterns = [
    path('disputes/', views.dispute_list, name='dispute_list'),
    path('disputes/<int:pk>/', views.dispute_detail, name='dispute_detail'),
    path('disputes/create/<int:order_id>/', views.create_dispute, name='create_dispute'),
    path('', include(router.urls)),
]
