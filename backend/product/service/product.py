from ..repositories.product import ProductRepositories

class ProductService():
    """
    Handle business logic for product operations
    """
    
    @staticmethod
    def list_all_products():
        return ProductRepositories.get_all_product()
    
    @staticmethod
    def get_product_details(product_id: str):
        return ProductRepositories.get_product_by_id(product_id)
    
    @staticmethod
    def list_product_reviews(product_id: str):
        return ProductRepositories.get_reviews_for_product(product_id)
    
    @staticmethod
    def create_product_review(product, user_id: str, user_first_name: str, rating: int, comment: str):
        return ProductRepositories.add_product_review(product, user_id, user_first_name, rating, comment)
    
    @staticmethod
    def reduce_product_stock(product, quantity: int):
        return ProductRepositories.deduct_product_stock(product, quantity)
    
    @staticmethod
    def list_categories():
        return ProductRepositories.get_category()