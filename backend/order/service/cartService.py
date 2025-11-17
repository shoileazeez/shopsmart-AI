from repositories.cart import CartRepositories

class CartService:
    """
    Handle business logic for cart operations
    """

    @staticmethod
    def get_or_create_cart(user_id: str):
        cart = CartRepositories.get_cart_by_user_id(user_id)
        if not cart:
            cart = CartRepositories.create_cart_for_user(user_id)
        return cart

    @staticmethod
    def add_item(user_id: str, product_id: str, quantity: int = 1):
        cart = CartService.get_or_create_cart(user_id)
        return CartRepositories.add_item_to_cart(cart, product_id, quantity)

    @staticmethod
    def remove_item(user_id: str, product_id: str):
        cart = CartService.get_or_create_cart(user_id)
        CartRepositories.remove_item_from_cart(cart, product_id)