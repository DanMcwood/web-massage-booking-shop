from django.shortcuts import render, redirect
from .forms import BookingForm
from django.contrib import messages
from .models import Booking
from django.utils import timezone

def booking(request):
    initial_data = {}
    if request.user.is_authenticated:
        # Получаем имя (из профиля или user)
        if hasattr(request.user, 'profile') and request.user.profile.full_name:
            initial_data['name'] = request.user.profile.full_name
        else:
            initial_data['name'] = request.user.get_full_name() or request.user.username
        initial_data['email'] = request.user.email

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Проверяем, свободна ли выбранная дата+время
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']

            exists = Booking.objects.filter(date=date, time=time).exists()
            if exists:
                messages.error(request, "Это время уже занято, выберите другое.")
            else:
                form.save()
                messages.success(request, "Запись успешно создана!")
                return redirect('thanks')
    else:
        form = BookingForm(initial=initial_data)

    return render(request, 'booking/booking_form.html', {'form': form})

def thanks(request):
    return render(request, 'booking/thanks.html')
