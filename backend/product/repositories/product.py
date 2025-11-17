from ..models import ProductModel, ProductReview, ProductCategory
from django.db.models import QuerySet

class ProductRepositories():
    """
    Hanlde all database query for product
    """
    
    @staticmethod
    def get_all_product() -> QuerySet[ProductModel]:
        return ProductModel.objects.filter(stock__gt=0)
    
    @staticmethod
    def get_product_by_id(product_id: str) -> ProductModel | None:
        try:
            product = ProductModel.objects.get(id=product_id)
            if product.stock > 0:
                return product
            return "product out of stock"
        except ProductModel.DoesNotExist:
            return None

    @staticmethod
    def get_reviews_for_product(product_id: str) -> QuerySet[ProductReview]:
        return ProductReview.objects.filter(product_id=product_id)
    
    @staticmethod
    def add_product_review(product: ProductModel, user_id: str, user_first_name: str, rating: int, comment: str) -> ProductReview:
        review = ProductReview.objects.create(
            product=product,
            user_id=user_id,
            user_first_name=user_first_name,
            rating=rating,
            comment=comment
        )
        return review

    @staticmethod
    def deduct_product_stock(product: ProductModel, quantity: int) -> None:
        product.deduct_stock(quantity)
    
    @staticmethod
    def get_category() -> QuerySet[ProductCategory]:
        return ProductCategory.objects.all()