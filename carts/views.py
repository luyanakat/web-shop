from itertools import product

from django.contrib.humanize.templatetags.humanize import intcomma
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from requests import models
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from carts.models import Cart, CartItem
from store.models import Product, Variation


# Create your views here.
def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id


def add_cart(request, product_id):
    product_get = Product.objects.get(id=product_id)
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variation = Variation.object.get(product=product_get, variation_category__iexact=key,
                                                 variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass

    try:
        cart_get = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart_get = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart_get.save()

    is_cart_item_exists = CartItem.objects.filter(
        product=product_get, cart=cart_get).exists()
    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product_get, cart=cart_get)
        # existing variation -> database
        # current variation -> product_variation
        # item_id -> database

        ex_var_list = []
        ids = []
        for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            ids.append(item.id)

        if product_variation in ex_var_list:
            index = ex_var_list.index(product_variation)
            item_id = ids[index]
            item = CartItem.objects.get(product=product_get, id=item_id)
            print("item", item.variations.name)
            item.quantity += 1
            item.save()
        else:
            item = CartItem.objects.create(product=product_get, quantity=1, cart=cart_get)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)

            # cart_item.quantity += 1
            item.save()
    else:
        cart_item = CartItem.objects.create(
            product=product_get,
            quantity=1,
            cart=cart_get,
        )
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()
    return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    cart_get = Cart.objects.get(cart_id=_cart_id(request))
    product_get = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product_get, cart=cart_get, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    cart_get = Cart.objects.get(cart_id=_cart_id(request))
    product_get = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product_get, cart=cart_get, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    grand_total = 0
    vat = 0
    try:
        cart_get = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart_get, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        vat = (8 * total) / 100
        grand_total = total + vat
    except ObjectDoesNotExist:
        pass

    context = {
        'total': intcomma("{:.0f}".format(total)),
        'quantity': quantity,
        'cart_items': cart_items,
        'vat': intcomma("{:.0f}".format(vat)),
        'grand_total': intcomma("{:.0f}".format(grand_total)),
    }

    return render(request, 'store/cart.html', context)
