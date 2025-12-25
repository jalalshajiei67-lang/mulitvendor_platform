from rest_framework import serializers
from .models import Seller
from products.serializers import SubcategorySerializer
from products.models import Subcategory


class SellerSerializer(serializers.ModelSerializer):
    """Serializer for Seller model"""
    working_fields = SubcategorySerializer(many=True, read_only=True)
    working_field_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Subcategory.objects.filter(is_active=True),
        source='working_fields',
        write_only=True,
        required=False
    )

    class Meta:
        model = Seller
        fields = [
            'id',
            'name',
            'company_name',
            'mobile_number',
            'phone',
            'working_fields',
            'working_field_ids',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SellerListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing sellers"""
    working_fields = serializers.SerializerMethodField()
    working_fields_display = serializers.SerializerMethodField()

    class Meta:
        model = Seller
        fields = [
            'id',
            'name',
            'company_name',
            'mobile_number',
            'phone',
            'working_fields',
            'working_fields_display'
        ]

    def get_working_fields(self, obj):
        """Return working fields as list of IDs"""
        return [wf.id for wf in obj.working_fields.all()]

    def get_working_fields_display(self, obj):
        """Return working fields as comma-separated names"""
        return obj.get_working_fields_display()


class SendSmsSerializer(serializers.Serializer):
    """Serializer for SMS sending request"""
    seller_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True,
        help_text='لیست شناسه‌های فروشندگان'
    )
    working_field_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        allow_empty=True,
        help_text='لیست شناسه‌های حوزه‌های کاری (اختیاری)'
    )

