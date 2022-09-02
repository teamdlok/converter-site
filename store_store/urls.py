from django.urls import path

from .views import *


app_name = 'store_store'

urlpatterns = [
    path('', all_products, name="all_products_url"),
    # path('<slug:by_category>, vi, name="by_category_url"',
    # path('<slug:by_category>/<slug:by_producttype>, vi, name="by_producttype_url"'),
    # path('<slug:by_category>/<slug:by_producttype>/<slug:by_productsubtype>, vi, name="by_productsubtype_url"'),
    path('product/<slug:id>', product_detail, name="product_detail_url"),
]