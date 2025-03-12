from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Dispute, DisputeEvidence
from .serializers import DisputeSerializer, DisputeEvidenceSerializer
from apps.orders.models import Order

class DisputeViewSet(viewsets.ModelViewSet):
    serializer_class = DisputeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Dispute.objects.all()
        
        if not user.is_staff:
            # 普通用户只能看到自己的纠纷
            queryset = queryset.filter(
                Q(complainant=user) | Q(order__seller=user)
            )
        
        # 状态筛选
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset

    def perform_create(self, serializer):
        order = get_object_or_404(Order, id=self.request.data.get('order'))
        if order.buyer != self.request.user:
            raise permissions.PermissionDenied("Only the buyer can create a dispute")
        
        dispute = serializer.save(complainant=self.request.user)
        
        # 处理证据文件
        evidence_files = self.request.FILES.getlist('evidence')
        for file in evidence_files:
            DisputeEvidence.objects.create(dispute=dispute, file=file)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        dispute = self.get_object()
        
        if not request.user.is_staff:
            return Response(
                {"error": "Only administrators can update dispute status"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        new_status = request.data.get('status')
        resolution = request.data.get('resolution')
        
        if new_status not in dict(Dispute.STATUS_CHOICES):
            return Response(
                {"error": "Invalid status"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        dispute.status = new_status
        if resolution:
            dispute.resolution = resolution
        dispute.save()
        
        return Response({
            "success": True,
            "message": f"Dispute status has been updated to {new_status}"
        })

    @action(detail=True, methods=['post'])
    def add_evidence(self, request, pk=None):
        dispute = self.get_object()
        
        if dispute.complainant != request.user and not request.user.is_staff:
            return Response(
                {"error": "No permission to add evidence"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        files = request.FILES.getlist('evidence')
        if not files:
            return Response(
                {"error": "No files uploaded"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        evidence_list = []
        for file in files:
            evidence = DisputeEvidence.objects.create(
                dispute=dispute,
                file=file
            )
            evidence_list.append(DisputeEvidenceSerializer(evidence).data)
        
        return Response({
            "success": True,
            "evidence": evidence_list
        })


@login_required
def dispute_list(request):
    user = request.user
    if user.is_staff:
        disputes = Dispute.objects.all()
    else:
        disputes = Dispute.objects.filter(
            Q(complainant=user) | Q(order__seller=user)
        )
    
    status = request.GET.get('status')
    if status:
        disputes = disputes.filter(status=status)
    
    return render(request, 'dispute_list.html', {'disputes': disputes})

@login_required
def dispute_detail(request, pk):
    dispute = get_object_or_404(Dispute, pk=pk)
    if not (request.user.is_staff or request.user == dispute.complainant or 
            request.user == dispute.order.seller):
        raise PermissionDenied
    return render(request, 'dispute_detail.html', {'dispute': dispute})

@login_required
def create_dispute(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.user != order.buyer:
        raise PermissionDenied("Only the buyer can create a dispute")
    return render(request, 'create_dispute.html', {'order': order})
