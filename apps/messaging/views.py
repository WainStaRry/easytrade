<<<<<<< HEAD
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer
from apps.users.models import CustomUser

=======
from rest_framework import viewsets, permissions
from .models import Message
from .serializers import MessageSerializer

# Viewset for messaging; users see messages they sent or received
>>>>>>> 1f1ec4b928cddfc092349168b2cf9870c33751a0
class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(sender=user) | Message.objects.filter(receiver=user)
<<<<<<< HEAD

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    @action(detail=False, methods=['GET'])
    def unread(self):
        user = self.request.user
        unread_messages = Message.objects.filter(receiver=user, is_read=False)
        serializer = self.get_serializer(unread_messages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def mark_as_read(self, request, pk=None):
        message = self.get_object()
        if message.receiver == request.user:
            message.is_read = True
            message.save()
            return Response({'status': 'message marked as read'})
        return Response({'error': 'not allowed'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['POST'])
    def send_message(self, request):
        try:
            receiver_username = request.data.get('receiver')
            content = request.data.get('content')
            subject = request.data.get('subject')
            
            receiver = CustomUser.objects.get(username=receiver_username)
            message = Message.objects.create(
                sender=request.user,
                receiver=receiver,
                content=content,
                subject=subject
            )
            
            return Response({
                'status': 'success',
                'content': content,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M')
            })
        except Exception as e:
            print(f"Error sending message: {str(e)}")  # 添加服务器端日志
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=400)

    @action(detail=True, methods=['POST'])
    def delete_message(self, request, pk=None):
        message = self.get_object()
        if message.sender == request.user or message.receiver == request.user:
            message.delete()
            return Response({'status': 'success'})
        return Response({'error': 'Permission denied'}, status=403)

# 添加分页功能
@login_required
def inbox_view(request):
    messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    return render(request, 'inbox.html', {'messages': messages})

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import models
from apps.users.models import CustomUser
from .models import Message

@login_required
def chat_view(request, user_id):
    chat_user = get_object_or_404(CustomUser, id=user_id)
    messages = Message.objects.filter(
        (models.Q(sender=request.user) & models.Q(receiver=chat_user)) |
        (models.Q(sender=chat_user) & models.Q(receiver=request.user))
    ).order_by('timestamp')
    
    return render(request, 'chat.html', {
        'chat_user': chat_user,
        'messages': messages
    })

@login_required
def sent_messages_view(request):
    messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    return render(request, 'inbox.html', {
        'messages': messages,
        'view_type': 'sent'
    })

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json

@login_required
@require_POST
def send_message(request):
    try:
        data = json.loads(request.body)
        receiver_id = data.get('receiver_id')
        content = data.get('content')
        
        receiver = CustomUser.objects.get(id=receiver_id)
        message = Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content,
            subject='Chat Message'
        )
        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required
def delete_conversation(request, user_id):
    try:
        other_user = get_object_or_404(CustomUser, id=user_id)
        Message.objects.filter(
            (models.Q(sender=request.user) & models.Q(receiver=other_user)) |
            (models.Q(sender=other_user) & models.Q(receiver=request.user))
        ).delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
=======
>>>>>>> 1f1ec4b928cddfc092349168b2cf9870c33751a0
