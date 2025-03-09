from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from apps.orders.models import Order
from apps.payments.models import PaymentRecord


@api_view(['POST'])
def create_payment_intent(request):
    """
    Simulate payment using user's account balance.
    Expects "order_id" in the POST data.
    """
    order_id = request.data.get("order_id")
    if not order_id:
        return Response({"error": "order_id is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        order = Order.objects.get(id=order_id, buyer=request.user)
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    # Calculate total amount from order items
    total_amount = sum(item.product.price * item.quantity for item in order.items.all())

    user = request.user
    if user.balance < total_amount:
        return Response({"error": "Insufficient balance."}, status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        # Deduct user's balance
        user.balance -= total_amount
        user.save()
        # Update order status to 'paid'
        order.status = "paid"
        order.save()
        # Create a payment record
        PaymentRecord.objects.create(order=order, user=user, amount=total_amount, status="success")

    return Response({
        "message": "Payment successful.",
        "remaining_balance": str(user.balance)
    })