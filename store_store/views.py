from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse, HttpResponseNotFound, FileResponse, StreamingHttpResponse

from .models import Category, ProductType, ProductSubType, Product


def all_products(request):
    product = get_object_or_404(Product, slug="best-priced-laptop")
    print(product.get_absolute_url())
    return HttpResponse(f"<h1>Готово 🦊 {product.id} </h1>")


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    print(product.productspecificationfields_set.__str__())
    return render(request, "Product_card_solo.html", {"product": product})
