from django.contrib.humanize.templatetags.humanize import intcomma
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404

from carts.models import CartItem
from carts.views import _cart_id
from category.models import Category
from store.models import Product


# Create your views here.
def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()

    formatted_products = [
        {
            'price': intcomma("{:.0f}".format(product.price)),
            'image': product.image,
            'product_name': product.product_name,
            'get_url': product.get_url(),
            'id': product.id,
        }
        for product in products
    ]
    context = {
        'products': formatted_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists
        return HttpResponse(in_cart)
        exit()
    except Exception as e:
        raise e
    formatted_product = {
        'price': intcomma("{:.0f}".format(single_product.price)),
        'image': single_product.image,
        'product_name': single_product.product_name,
        'description': single_product.description,
        'slug': single_product.slug,
        'get_url': single_product.get_url(),
        'stock': single_product.stock,
        'id': single_product.id,
    }
    context = {
        'single_product': formatted_product
    }
    return render(request, 'store/product_detail.html', context)
