from rest_framework import serializers
from .models import Order, OrderItem, Payment, OrderImage
from products.models import Product

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
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    images = OrderImageSerializer(many=True, read_only=True)
    buyer_username = serializers.CharField(source='buyer.username', read_only=True, allow_null=True)
    product_name = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True, allow_null=True)
    
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'buyer', 'buyer_username', 'status', 'total_amount', 
                  'shipping_address', 'shipping_phone', 'notes', 'is_paid', 'payment_method', 
                  'payment_date', 'items', 'payments', 'images', 'created_at', 'updated_at',
                  'is_rfq', 'first_name', 'last_name', 'company_name', 'phone_number', 
                  'unique_needs', 'category', 'category_name', 'product_name']
        read_only_fields = ['order_number', 'buyer', 'created_at', 'updated_at']
    
    def get_product_name(self, obj):
        """Get product name from first order item"""
        first_item = obj.items.first()
        if first_item:
            return first_item.product_name
        return None

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
        # Images will be extracted from request.FILES in the view
        
        product = Product.objects.get(id=product_id)
        category = None
        if category_id:
            from products.models import Category
            category = Category.objects.get(id=category_id)
        
        # Get buyer from request if authenticated, otherwise None
        buyer = self.context['request'].user if self.context['request'].user.is_authenticated else None
        
        # Create RFQ order
        order = Order.objects.create(
            buyer=buyer,
            is_rfq=True,
            status='pending',
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            company_name=validated_data['company_name'],
            phone_number=validated_data['phone_number'],
            unique_needs=validated_data['unique_needs'],
            category=category
        )
        
        # Create order item for the product
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,  # RFQ doesn't have quantity
            price=product.price
        )
        
        # Images will be handled in the view
        return order

