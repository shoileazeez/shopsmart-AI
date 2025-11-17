from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db import transaction
from ..models import OrderModel, OrderStatusHistory


# Status values that should clear a user's cart when set on an order
_CLEAR_CART_STATUSES = {"processing", "shipped"}


@receiver(pre_save, sender=OrderModel)
def order_pre_save(sender, instance, **kwargs):
    """Store previous status on the instance before saving so post_save can detect changes."""
    if not instance.pk:
        # New instance — no previous status
        instance._previous_status = None
    else:
        try:
            previous = sender.objects.get(pk=instance.pk)
            instance._previous_status = previous.status
        except sender.DoesNotExist:
            instance._previous_status = None


@receiver(post_save, sender=OrderModel)
def order_post_save(sender, instance, created, **kwargs):
    """Create an OrderStatusHistory entry when the order's status changed or on creation.

    We use transaction.on_commit to ensure the history row is created after the
    surrounding transaction commits successfully.
    """
    previous_status = getattr(instance, "_previous_status", None)

    # If created or status changed, record history
    if created or (previous_status != instance.status):
        def _create_history():
            OrderStatusHistory.objects.create(order=instance, status=instance.status)
            # If the order moved into 'processing', deduct stock for each item.
            if instance.status == 'processing':
                try:
                    from product.models import ProductModel

                    # Deduct stock in an atomic block to avoid partial updates.
                    with transaction.atomic():
                        for order_item in instance.items.all():
                            try:
                                prod = ProductModel.objects.get(pk=order_item.product_id)
                            except ProductModel.DoesNotExist:
                                # Product missing -> cancel the order
                                instance.update_status('cancelled')
                                return
                            try:
                                prod.deduct_stock(order_item.quantity)
                            except Exception:
                                # Insufficient stock or other error -> cancel order
                                instance.update_status('cancelled')
                                return
                except Exception:
                    # swallow exceptions to avoid breaking order flow; optionally log
                    try:
                        instance.update_status('cancelled')
                    except Exception:
                        pass
            # If the order moved into a status that should clear the user's cart,
            # remove the cart for that user (if any). Import models lazily to avoid
            # circular imports during app startup.
            if instance.status in _CLEAR_CART_STATUSES:
                try:
                    from order.models import CartModel
                    for cart in CartModel.objects.filter(user_id=instance.user_id):
                            # Clear and delete the CartItem instances for this cart.
                            # This removes items and keeps the empty CartModel row.
                            try:
                                cart.clear_and_delete_items()
                            except Exception:
                                pass
                except Exception:
                    # Avoid raising in signal; log if you have logging configured.
                    pass
        transaction.on_commit(_create_history)
