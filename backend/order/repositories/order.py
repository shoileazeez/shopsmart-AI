from decimal import Decimal
from django.db import transaction
from order.models import OrderModel, OrderStatusHistory, OrderItem
from typing import List

class OrderRepositories:
    """Handle database operations for orders."""

    @staticmethod
    def create_order(user_id: str, items: List[OrderItem], total_price: float) -> OrderModel:
        order = OrderModel.objects.create(user_id=user_id, total_price=Decimal(str(total_price)))
        order.items.set(items)
        order.calculate_total_price()
        return order

    @staticmethod
    def list_orders_for_user(user_id: str) -> List[OrderModel]:
        return OrderModel.objects.filter(user_id=user_id).order_by('-created_at')
    
    @staticmethod
    def get_order_by_id(order_id: str) -> OrderModel:
        try:
            return OrderModel.objects.get(id=order_id)
        except OrderModel.DoesNotExist:
            return None
    
    @staticmethod
    def get_order_history_for_user(user_id: str) -> List[OrderStatusHistory]:
        """
        Return status history rows for all orders that belong to the given user_id.

        Useful for building a user's full order timeline without fetching each
        order individually. Results are ordered by changed_at ascending.
        """
        return OrderStatusHistory.objects.filter(order__user_id=user_id).order_by('changed_at')

    @staticmethod
    def add_order_item(order: OrderModel, product_id: str, quantity: int, price_per_item: float) -> OrderItem:
        """
        Create an OrderItem and attach it to the provided OrderModel.

        This operation is done inside a transaction to ensure the item is
        created and the order total is updated atomically.
        """
        with transaction.atomic():
            item = OrderItem.objects.create(
                product_id=product_id,
                quantity=quantity,
                price_per_item=Decimal(str(price_per_item))
            )
            order.items.add(item)
            # Recalculate and persist the order total
            order.calculate_total_price()
        return item