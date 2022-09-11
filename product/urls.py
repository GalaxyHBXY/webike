from django.urls import path

from product.views import post_new_product, success, detail,product_search,product_filter

urlpatterns = [
    path('add_product', post_new_product, name='add_new_product'),
    path('success', success, name='add_product_success'),
    path('<int:id>', detail, name='product_detail'),
    path('search',product_search,name='product_search'),
    path('filter',product_filter,name='product_filter'),
]
