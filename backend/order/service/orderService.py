from repositories.order import OrderRepositories


class OrderService:
    """
    Handle business logic for order operations
    """

    @staticmethod
    def create_order(user_id: str, items: list, total_price: float):
        return OrderRepositories.create_order(user_id, items, total_price)

    @staticmethod
    def list_orders_for_user(user_id: str):
        return OrderRepositories.list_orders_for_user(user_id)

    @staticmethod
    def get_order_details(order_id: str):
        return OrderRepositories.get_order_by_id(order_id)

    @staticmethod
    def get_order_history_for_user(user_id: str):
        return OrderRepositories.get_order_history_for_user(user_id)

    @staticmethod
    def add_order_item(order, product_id: str, quantity: int, price_per_item: float):
        return OrderRepositories.add_order_item(order, product_id, quantity, price_per_item)