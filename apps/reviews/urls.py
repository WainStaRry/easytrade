<<<<<<< HEAD
from django.urls import path
from . import views

urlpatterns = [
    path('reviews/', views.review_home, name='product_reviews'),  # 添加主页路由
    path('product/<int:product_id>/review/', views.create_review, name='create_review'),
    path('product/<int:product_id>/reviews/', views.product_reviews, name='product_specific_reviews'),
=======
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet

router = DefaultRouter()
router.register(r'', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
>>>>>>> 1f1ec4b928cddfc092349168b2cf9870c33751a0
]
