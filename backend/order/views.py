from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (OrderSerializer, CartAddItemSerializer,
                          CartRemoveItemSerializer, CartSerializer,
                          CreateOrderSerializer, UpdateOrderStatusSerializer,
                          OrderStatusHistorySerializer)
from .service.orderService import OrderService
from .service.cartService import CartService
from .utils.user_id import fetch_user_id
from rest_framework.permissions import IsAuthenticated, AllowAny


class OrderListView(GenericAPIView):
    """
    API view to list all orders for the authenticated user
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = fetch_user_id(request)
        orders = OrderService.list_orders_for_user(user_id)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class OrderDetailView(GenericAPIView):
    """
    API view to get order details
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = OrderService.get_order_details(order_id)
        if not order:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class OrderHistoryView(GenericAPIView):
    """
    API view to get order history for the authenticated user
    """
    serializer_class = OrderStatusHistorySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = fetch_user_id(request)
        order_history = OrderService.get_order_history_for_user(user_id)
        serializer = self.get_serializer(order_history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CartAddItemView(GenericAPIView):
    """
    API view to add item to cart
    """
    serializer_class = CartAddItemSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        item = CartService.add_item(serializer.validated_data)
        return Response({"id": item.id, "product_id": item.product_id, "quantity": item.quantity}, status=status.HTTP_201_CREATED)
    
class CartRemoveItemView(GenericAPIView):
    """
    API view to remove item from cart
    """
    serializer_class = CartRemoveItemSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        CartService.remove_item(serializer.validated_data)
        return Response({"success": True, "message": "Item removed from cart."}, status=status.HTTP_200_OK)
    
class CartDetailView(GenericAPIView):
    """
    API view to get cart details
    """
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = CartService.get_or_create_cart(fetch_user_id(request))
        serializer = self.get_serializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CreateOrderView(GenericAPIView):
    """
    API view to create a new order
    """
    serializer_class = CreateOrderSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        order = OrderService.create_order(serializer.validated_data)
        order_serializer = OrderSerializer(order)
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)


class AddOrderItemView(GenericAPIView):
    """
    API view to add item to an existing order
    """
    serializer_class = CartAddItemSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        order = OrderService.get_order_details(order_id)
        if not order:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        item = OrderService.add_order_item(
            order,
            serializer.validated_data['product_id'],
            serializer.validated_data['quantity'],
            price_per_item=serializer.validated_data.get('price_per_item', 0.0)
        )
        return Response({"id": item.id, "product_id": item.product_id, "quantity": item.quantity}, status=status.HTTP_201_CREATED)