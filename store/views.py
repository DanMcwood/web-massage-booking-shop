from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Product, ProductCategory, Cart, CartItem
from django.views.decorators.http import require_POST
import json
from django.contrib import messages

def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart
    return request.session.get('cart', {})

def save_cart_session(request, cart_data):
    request.session['cart'] = cart_data

def product_list(request):
    category_slug = request.GET.get("category")
    categories = ProductCategory.objects.all()

    if category_slug and category_slug != 'all':
        products_all = Product.objects.filter(category__slug=category_slug)
    else:
        products_all = Product.objects.all()
        category_slug = 'all'

    paginator = Paginator(products_all, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    if request.user.is_authenticated:
        cart = get_cart(request)
        cart_items = cart.items.all()
        cart_dict = {str(item.product.id): item.quantity for item in cart_items}
        cart_count = sum(cart_dict.values())
    else:
        cart_dict = request.session.get('cart', {})
        cart_count = sum(cart_dict.values())

    return render(request, 'store/store.html', {
        'categories': categories,
        'active_category': category_slug,
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'cart_count': cart_count,
        'cart_dict': cart_dict,
    })

@require_POST
def add_to_cart(request):
    data = json.loads(request.body)
    product_id = str(data.get("product_id"))
    action = data.get("action")

    if not product_id or action not in ('add', 'remove_one'):
        return JsonResponse({"status": "error"}, status=400)

    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart = get_cart(request)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if action == 'add':
            if not created:
                item.quantity += 1
        elif action == 'remove_one':
            item.quantity -= 1

        if item.quantity <= 0:
            item.delete()
        else:
            item.save()

        count_for_product = item.quantity if item.pk else 0
        total_count = sum(i.quantity for i in cart.items.all())

    else:
        cart = request.session.get("cart", {})
        if action == 'add':
            cart[product_id] = cart.get(product_id, 0) + 1
        elif action == 'remove_one':
            if product_id in cart:
                cart[product_id] -= 1
                if cart[product_id] <= 0:
                    del cart[product_id]

        save_cart_session(request, cart)
        count_for_product = cart.get(product_id, 0)
        total_count = sum(cart.values())

    return JsonResponse({
        "status": "ok",
        "count_for_product": count_for_product,
        "total_count": total_count,
    })

def cart_view(request):
    cart_items = []
    total = 0

    if request.user.is_authenticated:
        cart = get_cart(request)
        items = cart.items.select_related('product')
        for item in items:
            subtotal = item.product.price * item.quantity
            total += subtotal
            cart_items.append({
                'product': item.product,
                'quantity': item.quantity,
                'subtotal': subtotal,
            })
        cart_count = sum(i.quantity for i in items)
    else:
        cart = request.session.get("cart", {})
        products = Product.objects.filter(id__in=cart.keys())
        for product in products:
            quantity = cart.get(str(product.id), 0)
            subtotal = product.price * quantity
            total += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
            })
        cart_count = sum(cart.values())

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total,
        'cart_count': cart_count,
    })

@require_POST
def remove_from_cart(request):
    product_id = request.POST.get("product_id")

    if request.user.is_authenticated:
        cart = get_cart(request)
        try:
            item = cart.items.get(product_id=product_id)
            item.delete()
        except CartItem.DoesNotExist:
            pass
    else:
        cart = request.session.get("cart", {})
        if product_id in cart:
            del cart[product_id]
            save_cart_session(request, cart)

    return JsonResponse({"status": "ok"})

@require_POST
def remove_multiple_from_cart(request):
    try:
        data = json.loads(request.body)
        product_ids = data.get('product_ids', [])
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

    if request.user.is_authenticated:
        cart = get_cart(request)
        cart.items.filter(product_id__in=product_ids).delete()
    else:
        cart = request.session.get("cart", {})
        for pid in product_ids:
            cart.pop(pid, None)
        save_cart_session(request, cart)

    return JsonResponse({"status": "ok"})
