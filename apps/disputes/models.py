from django.db import models
from apps.orders.models import Order
from apps.users.models import CustomUser

<<<<<<< HEAD
class DisputeEvidence(models.Model):
    dispute = models.ForeignKey('Dispute', on_delete=models.CASCADE, related_name='evidence')
    file = models.FileField(upload_to='dispute_evidence/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Dispute(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('processing', 'Processing'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected')
    ]

    REASON_CHOICES = [
        ('item_not_received', 'Item Not Received'),
        ('item_not_as_described', 'Item Not As Described'),
        ('wrong_item', 'Wrong Item Received'),
        ('damaged_item', 'Item Damaged'),
        ('other', 'Other')
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='disputes')
    complainant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='disputes')
    reason = models.CharField(max_length=50, choices=REASON_CHOICES)
    description = models.TextField(default='No description provided')  # 添加默认值
    # 或者允许为空：
    # description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    admin_notes = models.TextField(blank=True, null=True)
    resolution = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dispute #{self.id} for Order #{self.order.id}"

    class Meta:
        ordering = ['-created_at']
=======
class Dispute(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='disputes')
    complainant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='disputes')
    reason = models.TextField()
    status = models.CharField(max_length=20, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dispute for Order #{self.order.id} by {self.complainant.username}"
>>>>>>> 1f1ec4b928cddfc092349168b2cf9870c33751a0
