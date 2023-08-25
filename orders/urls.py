from django.urls import path
from .views import *

urlpatterns = [
    path('', OrderCreationListView.as_view(), name='orders'),
    path('<int:order_id>/', OrderDetailListView.as_view(), name='order_detail'),
    path('update_status/<int:order_id>/', UpdateOrderStatusView.as_view(), name='update_order_status'),
    path('user/<int:user_id>/orders/', UserOrderView.as_view(), name='users_orders'),
    path('user/<int:user_id>/order/<int:order_id>/', UserOrderDetailView.as_view(), name='user_specific_order_detail'),
    
    path('demo/', OrderView.as_view(), name='order_view'),
]