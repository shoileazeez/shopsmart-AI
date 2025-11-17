from rest_framework import serializers
from .models import CartModel, CartItem, OrderModel, OrderItem, OrderStatusHistory

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'
        
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = CartModel
        fields = '__all__'
        
class CartAddItemSerializer(serializers.Serializer):
    product_id = serializers.CharField(max_length=100)
    quantity = serializers.IntegerField(min_value=1)
    
    def validate_product_id(self, value):
        if not value:
            raise serializers.ValidationError("Product ID cannot be empty.")
        return value
    
class CartRemoveItemSerializer(serializers.Serializer):
    product_id = serializers.CharField(max_length=100)
    
    def validate_product_id(self, value):
        if not value:
            raise serializers.ValidationError("Product ID cannot be empty.")
        return value
    
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = '__all__'
        
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        
class CreateOrderSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=100)
    items = OrderItemSerializer(many=True)
    
    def validate_user_id(self, value):
        if not value:
            raise serializers.ValidationError("User ID cannot be empty.")
        return value

class UpdateOrderStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=OrderModel.STATUS_CHOICES)
    
    def validate_status(self, value):
        if value not in dict(OrderModel.STATUS_CHOICES):
            raise serializers.ValidationError("Invalid order status.")
        return value

class OrderStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatusHistory
        fields = '__all__'
        