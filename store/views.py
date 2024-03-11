from django.contrib.humanize.templatetags.humanize import intcomma
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from carts.models import CartItem
from carts.views import _cart_id
from category.models import Category
from store.models import Product


# Create your views here.
def store(request, category_slug=None):
    per_page = 9

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, per_page)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('updated_at')
        paginator = Paginator(products, per_page)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    for product in paged_products:
        product.price = intcomma("{:.0f}".format(product.price))

    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    single_product.price = intcomma("{:.0f}".format(single_product.price))
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    products = None
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_at').filter(Q(description__icontains=keyword) |
                                                                      Q(product_name__icontains=keyword))
    product_count = products.count()
    for product in products:
        product.price = intcomma("{:.0f}".format(product.price))
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)
