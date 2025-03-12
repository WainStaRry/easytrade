from rest_framework import serializers
from .models import Message
<<<<<<< HEAD
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
=======

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
>>>>>>> 1f1ec4b928cddfc092349168b2cf9870c33751a0
