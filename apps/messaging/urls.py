<<<<<<< HEAD
from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.inbox_view, name='inbox'),
    path('sent/', views.sent_messages_view, name='sent'),
    path('chat/<int:user_id>/', views.chat_view, name='chat'),
    path('chat/<int:user_id>/delete/', views.delete_conversation, name='delete_conversation'),
    path('messages/send/', views.send_message, name='send_message'),
=======
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet

router = DefaultRouter()
router.register(r'', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
>>>>>>> 1f1ec4b928cddfc092349168b2cf9870c33751a0
]
