from django.db import models
from decimal import Decimal
import uuid
# Canonical order status choices used across OrderModel and OrderStatusHistory
STATUS_CHOICES = (
    ("pending", "Pending"),
    ("processing", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
    ("cancelled", "Cancelled"),
)


class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_id = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"CartItem {self.product_id} (Quantity: {self.quantity})"
    
class CartModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=100, unique=True)
    items = models.ManyToManyField(CartItem)

    def __str__(self):
        return f"Cart for User {self.user_id}"
    
    def add_item(self, product_id: str, quantity: int) -> None:
        # When creating a new CartItem, provide the quantity in defaults so the
        # DB NOT NULL constraint on quantity is satisfied. Using defaults
        # ensures get_or_create will insert a complete row instead of creating
        # an object with a NULL quantity which raises IntegrityError on some
        # backends.
        item, created = CartItem.objects.get_or_create(
            product_id=product_id,
            defaults={"quantity": quantity}
        )

        if not created:
            # existing item: increment quantity
            item.quantity += quantity
            item.save()
        self.items.add(item)
        self.save()
    
    def remove_item(self, product_id: str) -> None:
        try:
            item = self.items.get(product_id=product_id)
            self.items.remove(item)
            item.delete()
            self.save()
        except CartItem.DoesNotExist:
            pass

    def clear_and_delete_items(self) -> None:
        """
        Remove all items from this cart and delete the corresponding CartItem
        instances. Use this when CartItem instances are not reused across carts.

        This method collects items first, deletes each CartItem (which also
        removes the through rows), and then saves the cart.
        """
        items = list(self.items.all())
        for item in items:
            try:
                # remove m2m link (not strictly required since deleting the
                # CartItem will remove the through row), but keep explicit
                # to be clear
                self.items.remove(item)
            except Exception:
                pass
            try:
                item.delete()
            except Exception:
                # ignore deletion errors here; callers can log if needed
                pass
        # ensure cart is saved and now empty
        self.save()

class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_id = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Item {self.product_id} (Quantity: {self.quantity})"
    
    def price(self) -> Decimal:
        """Return total price for this item as Decimal (quantity * unit price)."""
        # Ensure multiplication uses Decimal arithmetic
        return Decimal(self.quantity) * self.price_per_item

class OrderModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=100)
    items = models.ManyToManyField(OrderItem)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_id} by User {self.user_id}"
    
    def calculate_total_price(self) -> None:
        """Recalculate the order total from its items using Decimal arithmetic.

        Uses a Decimal starting value to ensure correct precision when summing.
        The result is quantized to two decimal places to match the field's
        decimal_places.
        """
        total = sum((item.price() for item in self.items.all()), Decimal('0'))
        # Quantize to 2 decimal places (like DecimalField with 2 decimal_places)
        total = total.quantize(Decimal('0.01'))
        self.total_price = total
        self.save()

    def update_status(self, new_status: str) -> None:
        self.status = new_status
        self.save()
        
class OrderStatusHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name='status_history')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order.order_id} changed to {self.status} at {self.changed_at}"
    
    # Note: status changes are tracked via signals (pre_save/post_save on OrderModel).
    # Do NOT override save() here to avoid implicit side-effects. The signal handlers
    # will create history rows when an OrderModel's status changes.