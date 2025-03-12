from django.urls import path
from . import views

urlpatterns = [
    path('reviews/', views.review_home, name='product_reviews'),  # 添加主页路由
    path('product/<int:product_id>/review/', views.create_review, name='create_review'),
    path('product/<int:product_id>/reviews/', views.product_reviews, name='product_specific_reviews'),
]
