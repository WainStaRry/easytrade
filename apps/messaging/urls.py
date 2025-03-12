from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.inbox_view, name='inbox'),
    path('sent/', views.sent_messages_view, name='sent'),
    path('chat/<int:user_id>/', views.chat_view, name='chat'),
    path('chat/<int:user_id>/delete/', views.delete_conversation, name='delete_conversation'),
    path('messages/send/', views.send_message, name='send_message'),
]
