from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:product_id>/reviews/', views.ProductReviewView.as_view(), name='product-reviews'),
    path('categories/', views.ProductCategoryView.as_view(), name='product-categories'),
]