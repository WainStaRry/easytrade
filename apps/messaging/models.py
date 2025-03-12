from django.db import models
from apps.users.models import CustomUser

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    subject = models.CharField(max_length=200, blank=True)
    related_product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']
