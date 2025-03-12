from django.db import models
from apps.users.models import CustomUser
from apps.orders.models import Order

class PaymentRecord(models.Model):
    """
    Model to record payment transactions using the user's account balance.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='success')  # e.g., 'success' or 'failed'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PaymentRecord(order={self.order.id}, user={self.user.username}, amount={self.amount}, status={self.status})"