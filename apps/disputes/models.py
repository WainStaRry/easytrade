from django.db import models
from apps.orders.models import Order
from apps.users.models import CustomUser

class Dispute(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='disputes')
    complainant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='disputes')
    reason = models.TextField()
    status = models.CharField(max_length=20, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dispute for Order #{self.order.id} by {self.complainant.username}"
