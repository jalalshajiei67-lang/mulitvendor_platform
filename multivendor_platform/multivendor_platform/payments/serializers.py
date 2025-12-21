"""
Serializers for Payment APIs
"""
from rest_framework import serializers
from .models import PremiumSubscriptionPayment, PaymentInvoice


class PremiumSubscriptionPaymentSerializer(serializers.ModelSerializer):
    """Serializer for premium subscription payments"""
    
    amount_toman = serializers.SerializerMethodField()
    billing_period_display = serializers.CharField(source='get_billing_period_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = PremiumSubscriptionPayment
        fields = [
            'id',
            'user',
            'user_username',
            'billing_period',
            'billing_period_display',
            'amount',
            'amount_toman',
            'track_id',
            'order_id',
            'ref_number',
            'card_number',
            'status',
            'status_display',
            'payment_method',
            'created_at',
            'paid_at',
            'verified_at',
            'description',
        ]
        read_only_fields = [
            'id',
            'user',
            'track_id',
            'order_id',
            'ref_number',
            'card_number',
            'status',
            'payment_method',
            'created_at',
            'paid_at',
            'verified_at',
        ]
    
    def get_amount_toman(self, obj):
        """Convert Rial to Toman"""
        return float(obj.get_amount_toman())


class PaymentInvoiceSerializer(serializers.ModelSerializer):
    """Serializer for payment invoices"""
    
    payment = PremiumSubscriptionPaymentSerializer(read_only=True)
    invoice_pdf_url = serializers.SerializerMethodField()
    
    class Meta:
        model = PaymentInvoice
        fields = [
            'id',
            'payment',
            'invoice_number',
            'issue_date',
            'due_date',
            'subtotal',
            'tax_amount',
            'total_amount',
            'invoice_pdf_url',
            'notes',
            'created_at',
        ]
        read_only_fields = '__all__'
    
    def get_invoice_pdf_url(self, obj):
        """Get invoice PDF URL"""
        if obj.invoice_pdf:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.invoice_pdf.url)
            return obj.invoice_pdf.url
        return None


class PaymentRequestSerializer(serializers.Serializer):
    """Serializer for payment request"""
    
    billing_period = serializers.ChoiceField(
        choices=['monthly', 'quarterly', 'semiannual', 'yearly'],
        default='monthly'
    )
    discount_code = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        max_length=50,
        help_text="Optional discount code"
    )


class PaymentCallbackSerializer(serializers.Serializer):
    """Serializer for Zibal callback data"""
    
    trackId = serializers.IntegerField()
    success = serializers.IntegerField()
    status = serializers.IntegerField()
    orderId = serializers.CharField(required=False, allow_blank=True)

