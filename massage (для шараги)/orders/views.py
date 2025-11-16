from django.shortcuts import render, redirect
from .forms import OrderForm
from store.models import Product
from .models import Order, OrderItem
from store.models import Cart, CartItem
import json
import ast 

def order_create(request):
    print('--- order_create START ---')

    if request.user.is_authenticated:
        cart_obj, _ = Cart.objects.get_or_create(user=request.user)
        all_cart_items = cart_obj.items.select_related('product')
        cart_dict = {str(item.product.id): item.quantity for item in all_cart_items}
    else:
        cart_dict = request.session.get('cart', {})

    print(f"cart_dict на сервере: {cart_dict}")

    # Форма автозаполнения
    initial_data = {}
    if request.user.is_authenticated:
        user = request.user
        profile = getattr(user, 'profile', None)
        if profile:
            initial_data['email'] = user.email or ''
            initial_data['full_name'] = profile.full_name or ''
            initial_data['address'] = profile.address or ''
            initial_data['city'] = profile.city or ''

    print(f"Initial data для формы: {initial_data}")

    if request.method == 'POST':
        post_data = request.POST.copy()
        if 'payment_method' not in post_data:
            post_data['payment_method'] = 'cash'

        for key, value in initial_data.items():
            if key not in post_data:
                post_data[key] = value

        form = OrderForm(post_data)

        cart_json_raw = request.POST.get('cart_json', '{}')
        print(f"cart_json из POST (сырой): {cart_json_raw}")

        if isinstance(cart_json_raw, dict):
            selected_cart_dict = cart_json_raw
        else:
            try:
                selected_cart_dict = json.loads(cart_json_raw)
            except json.JSONDecodeError:
                try:
                    selected_cart_dict = ast.literal_eval(cart_json_raw)  # <--- тут парсим пайтоновский словарь
                except Exception as e:
                    print(f"Ошибка парсинга cart_json через ast.literal_eval: {e}")
                    selected_cart_dict = {}

        print(f"selected_cart_dict (парсинг cart_json): {selected_cart_dict}")

        selected_ids = list(selected_cart_dict.keys())
        print(f"Выбранные ID из cart_json: {selected_ids}")

        # Фильтруем по реальному cart_dict на сервере
        filtered_selected_cart = {
            pid: int(selected_cart_dict[pid])
            for pid in selected_ids if pid in cart_dict
        }
        print(f"filtered_selected_cart после фильтрации по cart_dict: {filtered_selected_cart}")

        if form.is_valid():
            if 'confirm_order' in post_data:
                print("Создаем заказ")
                order = form.save(commit=False)
                order.user = request.user if request.user.is_authenticated else None
                order.save()

                for pid, qty in filtered_selected_cart.items():
                    try:
                        product = Product.objects.get(id=int(pid))
                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            quantity=qty,
                            price=product.price,
                        )
                    except Product.DoesNotExist:
                        print(f'Товар с ID {pid} не найден')

                # Удаляем только выбранные товары из корзины
                if request.user.is_authenticated:
                    cart_obj.items.filter(product_id__in=filtered_selected_cart.keys()).delete()
                    print(f"Удалены товары из корзины пользователя: {list(filtered_selected_cart.keys())}")
                else:
                    for pid in filtered_selected_cart.keys():
                        cart_dict.pop(pid, None)
                    request.session['cart'] = cart_dict
                    request.session.modified = True
                    print(f"Обновленная корзина в сессии: {cart_dict}")

                return redirect('order_success')

            else:
                print("Показываем подтверждение")
                items = []
                total = 0
                count = 0
                for pid, qty in filtered_selected_cart.items():
                    try:
                        product = Product.objects.get(id=int(pid))
                        subtotal = product.price * qty
                        items.append({'product': product, 'quantity': qty, 'subtotal': subtotal})
                        total += subtotal
                        count += qty
                    except Product.DoesNotExist:
                        print(f'Товар с ID {pid} не найден')

                return render(request, 'orders/order.html', {
                    'form': form,
                    'cart_items': items,
                    'total': total,
                    'count': count,
                    'cart_json': filtered_selected_cart,
                    'confirm_step': True,
                })

        else:
            print("Форма не валидна!")
            print(form.errors)

    else:
        form = OrderForm(initial=initial_data)

    # Отображаем полную корзину при GET-запросе
    items = []
    total = 0
    count = 0
    for pid, qty in cart_dict.items():
        try:
            product = Product.objects.get(id=int(pid))
            subtotal = product.price * qty
            items.append({'product': product, 'quantity': qty, 'subtotal': subtotal})
            total += subtotal
            count += qty
        except Product.DoesNotExist:
            print(f'Товар с ID {pid} не найден')

    print(f"Данные для отображения полной корзины: count={count}, total={total}")

    return render(request, 'orders/order.html', {
        'form': form,
        'cart_items': items,
        'total': total,
        'count': count,
        'cart_json': cart_dict,
        'confirm_step': False,
    })


def order_success(request):
    return render(request, 'orders/order_success.html')
