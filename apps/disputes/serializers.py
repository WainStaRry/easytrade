from rest_framework import serializers
<<<<<<< HEAD
from .models import Dispute, DisputeEvidence

class DisputeEvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisputeEvidence
        fields = ['id', 'file', 'uploaded_at']

class DisputeSerializer(serializers.ModelSerializer):
    evidence = DisputeEvidenceSerializer(many=True, read_only=True)
    complainant_name = serializers.CharField(source='complainant.username', read_only=True)
    order_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Dispute
        fields = ['id', 'order', 'complainant', 'reason', 'description', 
                 'status', 'created_at', 'updated_at', 'evidence',
                 'complainant_name', 'order_info', 'resolution']
        read_only_fields = ['complainant', 'status', 'resolution']

    def get_order_info(self, obj):
        return {
            'order_id': obj.order.id,
            'product_name': obj.order.product.title,
            'total_amount': str(obj.order.total_amount)
        }
=======
from .models import Dispute

class DisputeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispute
        fields = '__all__'
>>>>>>> 1f1ec4b928cddfc092349168b2cf9870c33751a0
