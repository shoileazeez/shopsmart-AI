from django.db import models
import uuid

class ProductCategory(models.Model):
    CATEGORIES_CHOICES = [
        ('electronics', 'Electronics'),
        ('fashion', 'Fashion'),
        ('home_appliances', 'Home Appliances'),
        ('books', 'Books'),
        ('toys', 'Toys'),
        ('sports', 'Sports'),
        ('beauty', 'Beauty'),
        ('automotive', 'Automotive'),
        ('groceries', 'Groceries'),
        ('health', 'Health'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, choices=CATEGORIES_CHOICES, unique=True)
    
    def __str__(self):
        return self.name

class ProductModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField()
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def deduct_stock(self, quantity):
        if quantity > self.stock:
            raise ValueError("Insufficient stock available.")
        self.stock -= quantity
        self.save() 
        
    def __str__(self):
        return self.name
    
class ProductReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='reviews')
    user_id = models.UUIDField(db_index=True)
    user_first_name = models.CharField()
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Review for {self.product.name} by {self.user_id}'
