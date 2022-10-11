from django.urls import path

from product.views import add_new_product, success, detail, product_search, product_filter, product_ship, delete_product

urlpatterns = [
    path('add_new_product', add_new_product, name='add_new_product'),
    path('delete_product', delete_product, name='delete_product'),
    path('success', success, name='add_product_success'),
    path('<int:id>', detail, name='product_detail'),
    path('search', product_search, name='product_search'),
    path('filter', product_filter, name='product_filter'),
    path('ship', product_ship, name='product_ship')
]
