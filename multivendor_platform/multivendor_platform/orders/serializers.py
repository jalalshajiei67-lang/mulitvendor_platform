from rest_framework import serializers
from .models import Order, OrderItem, Payment, OrderImage
from products.models import Product
from products.utils import build_absolute_uri

class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product_id', 'product_name', 'quantity', 'price', 'subtotal', 'seller']
        read_only_fields = ['product_name', 'subtotal', 'seller']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'amount', 'payment_method', 'transaction_id', 'status', 'notes', 'created_at']
        read_only_fields = ['created_at']

class OrderImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderImage
        fields = ['id', 'image', 'image_url', 'alt_text', 'created_at']
        read_only_fields = ['created_at']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            return build_absolute_uri(request, obj.image.url)
        return None

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    images = OrderImageSerializer(many=True, read_only=True)
    buyer_display_name = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True, allow_null=True)
    suppliers = serializers.SerializerMethodField()
    lead_source_display = serializers.CharField(source='get_lead_source_display', read_only=True)
    contact_revealed = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'buyer', 'buyer_display_name', 'status', 'total_amount', 
                  'shipping_address', 'shipping_phone', 'notes', 'is_paid', 'payment_method',
                  'payment_date', 'items', 'payments', 'images', 'created_at', 'updated_at',
                  'is_rfq', 'is_free', 'first_name', 'last_name', 'company_name', 'phone_number', 'email',
                  'unique_needs', 'category', 'category_name', 'product_name', 'lead_source',
                  'lead_source_display', 'suppliers', 'first_viewed_at', 'first_responded_at',
                  'contact_revealed',
                  'response_points_awarded', 'response_speed_bucket']
        read_only_fields = ['order_number', 'buyer', 'created_at', 'updated_at']
    
    def get_buyer_display_name(self, obj):
        """Get buyer display name: first_name last_name"""
        if not obj.buyer:
            return None
        name_parts = [obj.buyer.first_name, obj.buyer.last_name]
        return ' '.join(filter(None, name_parts)) or obj.buyer.username
    
    def get_suppliers(self, obj):
        """Get supplier IDs and names"""
        return [{'id': s.id, 'name': s.name} for s in obj.suppliers.all()]
    
    def get_product_name(self, obj):
        """Get product name from first order item"""
        first_item = obj.items.first()
        if first_item:
            return first_item.product_name
        return None

    def get_contact_revealed(self, obj):
        # Context can pass explicit flag or set of viewed ids
        if self.context.get('contact_revealed', False):
            return True
        viewed_ids = self.context.get('viewed_order_ids')
        if viewed_ids is not None:
            return obj.id in viewed_ids
        return False

    def to_representation(self, instance):
        """
        Mask contact fields for RFQs unless show_full_contact is explicitly requested
        (used for vendor list; reveal endpoint passes show_full_contact=True).
        """
        data = super().to_representation(instance)
        show_full = self.context.get('show_full_contact', True)
        if instance.is_rfq and not show_full:
            data['first_name'] = self._mask_name(instance.first_name)
            data['last_name'] = self._mask_name(instance.last_name)
            data['phone_number'] = self._mask_phone(instance.phone_number)
            data['email'] = None
        return data

    @staticmethod
    def _mask_name(value: str):
        if not value:
            return None
        return f"{value[:1]}..." if len(value) > 1 else value

    @staticmethod
    def _mask_phone(value: str):
        if not value:
            return None
        digits = str(value)
        if len(digits) <= 4:
            return "***"
        return f"{digits[:4]}****{digits[-2:]}"

class CreateOrderSerializer(serializers.Serializer):
    items = serializers.ListField(
        child=serializers.DictField(),
        write_only=True
    )
    shipping_address = serializers.CharField()
    shipping_phone = serializers.CharField(max_length=20)
    notes = serializers.CharField(required=False, allow_blank=True)
    payment_method = serializers.CharField(max_length=50, required=False)
    
    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("At least one item is required")
        
        for item in value:
            if 'product_id' not in item or 'quantity' not in item:
                raise serializers.ValidationError("Each item must have product_id and quantity")
            
            # Validate product exists and has enough stock
            try:
                product = Product.objects.get(id=item['product_id'])
                if product.stock < item['quantity']:
                    raise serializers.ValidationError(f"Not enough stock for {product.name}")
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"Product with id {item['product_id']} does not exist")
        
        return value
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        buyer = self.context['request'].user
        
        # Calculate total amount
        total_amount = 0
        for item_data in items_data:
            product = Product.objects.get(id=item_data['product_id'])
            total_amount += product.price * item_data['quantity']
        
        # Create order
        order = Order.objects.create(
            buyer=buyer,
            total_amount=total_amount,
            shipping_address=validated_data['shipping_address'],
            shipping_phone=validated_data['shipping_phone'],
            notes=validated_data.get('notes', ''),
            payment_method=validated_data.get('payment_method', '')
        )
        
        # Create order items
        for item_data in items_data:
            product = Product.objects.get(id=item_data['product_id'])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data['quantity'],
                price=product.price
            )
            
            # Decrease stock
            product.stock -= item_data['quantity']
            product.save()
        
        return order

class CreateRFQSerializer(serializers.Serializer):
    """Serializer for creating RFQ (Request for Quotation)"""
    product_id = serializers.IntegerField(required=True, help_text="Product ID for the RFQ")
    category_id = serializers.IntegerField(required=False, allow_null=True, help_text="Category ID (if submitted from category page)")
    is_free = serializers.BooleanField(required=False, default=False, help_text="If true and no category is provided, lead is visible to all sellers")
    first_name = serializers.CharField(max_length=100, required=True)
    last_name = serializers.CharField(max_length=100, required=True)
    company_name = serializers.CharField(max_length=200, required=True)
    phone_number = serializers.CharField(max_length=20, required=True)
    unique_needs = serializers.CharField(required=True, allow_blank=True)
    # Images will be handled separately in the view for multipart/form-data
    
    def validate_product_id(self, value):
        try:
            product = Product.objects.get(id=value, is_active=True)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found or inactive")
        return value
    
    def validate_category_id(self, value):
        if value is not None:
            from products.models import Category
            try:
                Category.objects.get(id=value)
            except Category.DoesNotExist:
                raise serializers.ValidationError("Category not found")
        return value
    
    def create(self, validated_data):
        product_id = validated_data.pop('product_id')
        category_id = validated_data.pop('category_id', None)
        is_free = validated_data.pop('is_free', False)
        # Images will be extracted from request.FILES in the view
        
        product = Product.objects.get(id=product_id)
        category = None
        if category_id:
            from products.models import Category
            category = Category.objects.get(id=category_id)
        else:
            is_free = True  # No category means this is a free/open lead
        
        # Get buyer from request if authenticated, otherwise None
        buyer = self.context['request'].user if self.context['request'].user.is_authenticated else None
        
        # Create RFQ order
        order = Order.objects.create(
            buyer=buyer,
            is_rfq=True,
            is_free=is_free,
            status='pending',
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            company_name=validated_data['company_name'],
            phone_number=validated_data['phone_number'],
            unique_needs=validated_data['unique_needs'],
            category=category
        )
        
        # Create order item for the product
        # Convert price from PositiveBigIntegerField to Decimal
        from decimal import Decimal
        product_price = Decimal(str(product.price)) if product.price else Decimal('0')
        
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,  # RFQ doesn't have quantity
            price=product_price  # Store actual product price for RFQ
        )
        
        # Images will be handled in the view
        return order

class AdminCreateRFQSerializer(serializers.Serializer):
    """Serializer for admin to create manual RFQ/lead"""
    product_id = serializers.IntegerField(required=False, allow_null=True, help_text="Product ID (optional)")
    category_id = serializers.IntegerField(required=False, allow_null=True, help_text="Category ID (required unless lead is free)")
    is_free = serializers.BooleanField(required=False, default=False, help_text="Mark as free/open lead visible to all sellers")
    first_name = serializers.CharField(max_length=100, required=True)
    last_name = serializers.CharField(max_length=100, required=True)
    company_name = serializers.CharField(max_length=200, required=True)
    phone_number = serializers.CharField(max_length=20, required=True)
    email = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
    unique_needs = serializers.CharField(required=False, allow_blank=True)
    lead_source = serializers.ChoiceField(choices=[('phone', 'Phone'), ('whatsapp', 'WhatsApp'), ('instagram', 'Instagram')], required=True)
    supplier_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        allow_empty=True,
        help_text="List of supplier IDs to send this RFQ to (optional, will auto-match if not provided)"
    )
    # Images will be handled separately in the view for multipart/form-data
    
    def validate_category_id(self, value):
        if value is None:
            return value
        from products.models import Category
        try:
            Category.objects.get(id=value)
        except Category.DoesNotExist:
            raise serializers.ValidationError("Category not found")
        return value
    
    def validate_product_id(self, value):
        if value is not None:
            try:
                Product.objects.get(id=value, is_active=True)
            except Product.DoesNotExist:
                raise serializers.ValidationError("Product not found or inactive")
        return value
    
    def validate_supplier_ids(self, value):
        if value:
            from users.models import Supplier
            for supplier_id in value:
                try:
                    Supplier.objects.get(id=supplier_id, is_active=True)
                except Supplier.DoesNotExist:
                    raise serializers.ValidationError(f"Supplier with id {supplier_id} not found or inactive")
        return value

    def validate(self, attrs):
        is_free = attrs.get('is_free', False)
        category_id = attrs.get('category_id')
        product_id = attrs.get('product_id')

        if product_id:
            # Product-specific leads should not be treated as free
            attrs['is_free'] = False

        if not is_free and not category_id:
            raise serializers.ValidationError("Category is required unless the lead is marked as free.")

        return attrs

