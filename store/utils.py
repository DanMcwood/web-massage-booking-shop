from .models import Cart, CartItem, Product

def get_or_create_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart

def add_product_to_cart(user, product_id, quantity=1):
    cart = get_or_create_cart(user)
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()
    return cart_item

def remove_one_product_from_cart(user, product_id):
    cart = get_or_create_cart(user)
    try:
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass
