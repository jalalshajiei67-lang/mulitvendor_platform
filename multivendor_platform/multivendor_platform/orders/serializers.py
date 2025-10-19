from rest_framework import serializers
from .models import Order, OrderItem, Payment
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

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    buyer_username = serializers.CharField(source='buyer.username', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'buyer', 'buyer_username', 'status', 'total_amount', 
                  'shipping_address', 'shipping_phone', 'notes', 'is_paid', 'payment_method', 
                  'payment_date', 'items', 'payments', 'created_at', 'updated_at']
        read_only_fields = ['order_number', 'buyer', 'created_at', 'updated_at']

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

