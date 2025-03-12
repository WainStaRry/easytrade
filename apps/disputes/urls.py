from django.urls import path, include
from rest_framework.routers import DefaultRouter
<<<<<<< HEAD
from . import views

router = DefaultRouter()
router.register(r'api/disputes', views.DisputeViewSet, basename='dispute')

urlpatterns = [
    path('disputes/', views.dispute_list, name='dispute_list'),
    path('disputes/<int:pk>/', views.dispute_detail, name='dispute_detail'),
    path('disputes/create/<int:order_id>/', views.create_dispute, name='create_dispute'),
=======
from .views import DisputeViewSet

router = DefaultRouter()
router.register(r'', DisputeViewSet, basename='dispute')

urlpatterns = [
>>>>>>> 1f1ec4b928cddfc092349168b2cf9870c33751a0
    path('', include(router.urls)),
]
