from django.shortcuts import render, get_object_or_404
from services.models import Category, Service
from booking.forms import BookingForm  # если форма записи используется

def home(request):
    form = BookingForm()  # если используешь форму записи
    categories = Category.objects.prefetch_related('services').all()

    # допустим, catalog — это список всех категорий или services
    catalog = categories  # или другой список, если есть логика

    cart_items = []  # если нет корзины пока — временно так
    total = 0        # сумма корзины

    return render(request, 'home/base.html', {
        'form': form,
        'catalog': catalog,
        'categories': categories,
        'cart_items': cart_items,
        'cart_total': total,
    })

from django.shortcuts import render
from .models import Category

def services(request):
    categories = Category.objects.prefetch_related('services').all()
    return render(request, 'services/services.html', {'categories': categories})

def services_list(request):
    categories = Category.objects.prefetch_related('services__details').all()
    
    for category in categories:
        for service in category.services.all():
            service.details_total_price = sum(detail.price for detail in service.details.all())
            service.details_list = service.details.all()

    return render(request, 'services/services_list.html', {'categories': categories})

def service_detail(request, service_slug):
    service = get_object_or_404(Service, slug=service_slug)
    details = service.details.all()
    return render(request, 'services/service_detail.html', {'service': service, 'details': details})