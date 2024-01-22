from itertools import product

from django.shortcuts import render, redirect

from carts.models import Cart, CartItem
from store.models import Product


# Create your views here.
def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id


def add_cart(request, product_id):
    product_id = Product.objects.get(id=product_id)
    try:
        new_cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        new_cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    new_cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        cart_item.save()
    return redirect('cart')

def cart(request):
    return render(request, 'store/cart.html')
