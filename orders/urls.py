from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Customer Cart View (using the DB-backed view)
    path('cart/', views.cart_detail, name='cart'),

    # Cart Modification Endpoints
    path('add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),  # NEW: Quantity Update

    # Checkout View (Future step)
    # path('checkout/', views.checkout_view, name='checkout'),
]