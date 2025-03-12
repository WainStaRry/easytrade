from rest_framework import serializers
from .models import Message
from apps.users.serializers import UserSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender_detail = UserSerializer(source='sender', read_only=True)
    receiver_detail = UserSerializer(source='receiver', read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 
                 'is_read', 'subject', 'related_product',
                 'sender_detail', 'receiver_detail']
        read_only_fields = ['sender', 'timestamp']
