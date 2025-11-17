from  django.urls import path
from .views import (OrderListView, OrderDetailView, OrderHistoryView,
                    CartAddItemView, CartRemoveItemView, CartDetailView,
                    CreateOrderView, AddOrderItemView)


urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<str:order_id>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/history/', OrderHistoryView.as_view(), name='order-history'),
    path('cart/add-item/', CartAddItemView.as_view(), name='cart-add-item'),
    path('cart/remove-item/', CartRemoveItemView.as_view(), name='cart-remove-item'),
    path('cart/', CartDetailView.as_view(), name='cart-detail'),
    path('orders/create/', CreateOrderView.as_view(), name='create-order'), 
    path('orders/<str:order_id>/add-item/', AddOrderItemView.as_view(), name='add-order-item'),
]