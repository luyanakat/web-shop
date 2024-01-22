from django.shortcuts import render
from store.models import Product
from django.contrib.humanize.templatetags.humanize import intcomma


def home(request):
    products = Product.objects.all().filter(is_available=True)
    formatted_products = [
        {
            'price': intcomma("{:.0f}".format(product.price)),
            'image': product.image,
            'product_name': product.product_name,
            'get_url': product.get_url(),
            'description': product.description,
            'stock': product.stock,
        }
        for product in products
    ]
    context = {
        'products': formatted_products,
    }
    print(formatted_products)
    return render(request, 'home.html', context)
