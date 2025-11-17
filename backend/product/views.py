from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from .service.user import get_user_first_name
from backend.utils.get_user_id import get_user_info_from_request
from .service.product import ProductService
from .serializers import ProductSerializer, ProductReviewSerializer, ProductCategorySerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


class ProductListView(GenericAPIView):
    """
    API view to list all products
    """
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    
    def get(self, request):
        products = ProductService.list_all_products()
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductDetailView(GenericAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get(self, request, pk):
        product = ProductService.get_product_details(pk)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductReviewView(GenericAPIView):
    serializer_class = ProductReviewSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        reviews = ProductService.list_product_reviews(product_id)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, product_id):
        product = ProductService.get_product_details(product_id)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Ensure we have an authenticated user and extract id/first_name via helper
        user_info = get_user_info_from_request(request)
        if not user_info:
            return Response({"error": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = user_info.get("id")
        # Prefer first_name from request payload; fallback to service lookup
        user_first_name = user_info.get("first_name") or get_user_first_name(user_id, request=request)
        rating = request.data.get('rating')
        comment = request.data.get('comment')

        review = ProductService.create_product_review(
            product, user_id, user_first_name, rating, comment
        )
        serializer = self.get_serializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductCategoryView(GenericAPIView):
    serializer_class = ProductCategorySerializer
    permission_classes = [AllowAny]

    def get(self, request):
        categories = ProductService.list_categories()
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)