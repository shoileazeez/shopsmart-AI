from order.models import CartItem, CartModel
from typing import Optional
from django.db import IntegrityError


class CartRepositories:
    """Handle database operations for carts."""

    @staticmethod
    def get_cart_by_user_id(user_id: str) -> Optional[CartModel]:
        try:
            return CartModel.objects.get(user_id=user_id)
        except CartModel.DoesNotExist:
            return None

    @staticmethod
    def create_cart_for_user(user_id: str) -> CartModel:
        """
        Create a cart for the given user_id or return the existing one.

        Uses get_or_create to avoid UNIQUE constraint errors when multiple
        requests attempt to create a cart concurrently for the same user.
        """
        try:
            cart, _ = CartModel.objects.get_or_create(user_id=user_id)
            return cart
        except IntegrityError:
            # Fallback: another process likely created the cart concurrently.
            # Retrieve and return the existing cart.
            return CartModel.objects.get(user_id=user_id)

    @staticmethod
    def add_item_to_cart(cart: CartModel, product_id: str, quantity: int = 1) -> CartItem:
        """
        Add an item to the given cart. This will reuse the CartModel.add_item
        logic (which creates or updates a CartItem and links it to the cart).

        Returns the CartItem instance that was added/updated.
        """
        # Delegate to the model method which handles get_or_create and quantity update
        cart.add_item(product_id=product_id, quantity=quantity)

        # After adding, return the CartItem instance from the cart relationship
        return cart.items.get(product_id=product_id)

    @staticmethod
    def remove_item_from_cart(cart: CartModel, product_id: str) -> None:
        """Remove the item with `product_id` from cart (if present)."""
        cart.remove_item(product_id)