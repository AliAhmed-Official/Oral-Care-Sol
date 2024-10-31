from django.urls import path
from OCS_APP import views

app_name = 'OCS_APP'

urlpatterns = [
    path('', views.index, name='index'),
    path('category/', views.category_list_view, name='category-list'),
    path('category/<cid>/', views.category_products_list_view, name='category-product-list'),
    path('product/<pid>/', views.product_detail_view, name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('search/', views.search_view, name='search'),
    path('cart/', views.cart_view, name='cart'),
    path('delete-from-cart/', views.delete_item_from_cart, name='delete-from-cart'),
    path('update-cart/', views.update_cart, name='update-cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('payment-completed/<inv_id>/<pay_method>/', views.payment_completed_view, name='payment-completed'),
    path('payment-failed/', views.payment_failed_view, name='payment-failed'),
    path('dashboard/', views.customer_dashboard, name='dashboard'),
    path('dashboard/order/<int:id>', views.order_detail, name='order-detail'),
    path('contact-us/', views.contact_us, name='contact-us'),
    path('products/tag/<slug:tag_slug>/', views.tag_list, name='tags'),
    path('make-default-address/', views.make_address_default, name='make-default-address'),
    path('delete-address/', views.delete_address, name='delete-address'),
    path('shop/', views.shop_view, name='shop'),
    path('add-review/<int:pid>/', views.ajax_add_review, name='add-review'),
    
    path('my/', views.my, name='my'),
]

handler404 = 'OCS_APP.views.custom_404_view'