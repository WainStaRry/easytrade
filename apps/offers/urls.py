from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'api/offers', views.OfferViewSet, basename='offer')

urlpatterns = [
    path('product/<int:product_id>/make-offer/', views.make_offer, name='make_offer'),
    path('offers/received/', views.offers_received, name='offers_received'),
    path('offers/sent/', views.offers_sent, name='offers_sent'),
    path('', include(router.urls)),
]
