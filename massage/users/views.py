from django.shortcuts import render, redirect
from django.contrib.auth import login
from users.forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.contrib.auth.models import User
from .tokens import email_verification_token
from .models import UserProfile

def send_verification_email(request, user):
    token = email_verification_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    domain = get_current_site(request).domain
    link = f"http://{domain}/profile/verify-email/{uid}/{token}/"
    message = render_to_string('users/email_verify.html', {
        'link': link,
        'user': user
    })
    send_mail(
        'Подтвердите почту',
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email]
    )

def profile_auth_view(request):
    from_page = request.GET.get("from", "")

    if request.user.is_authenticated:
        # Загрузим покупки и записи для текущего пользователя
        purchases = Order.objects.filter(email=request.user.email).order_by('-created_at')
        bookings = Booking.objects.filter(email=request.user.email).order_by('-date', '-time')

        return render(request, 'users/profile_logged.html', {
            'from_page': from_page,
            'purchases': purchases,
            'bookings': bookings,
        })

    if request.method == 'POST':
        if 'register' in request.POST:
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()
                UserProfile.objects.get_or_create(user=user)
                send_verification_email(request, user)
                login(request, user)
                messages.info(request, "Подтвердите вашу почту через ссылку в письме.")
                return redirect('profile')

        elif 'login' in request.POST:
            form = LoginForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                if not user.profile.is_email_verified:
                    messages.warning(request, "Почта не подтверждена. Проверьте email.")
                    send_verification_email(request, user)
                    return redirect('profile')

                login(request, user)
                return redirect('profile')
            else:
                messages.error(request, "Неверный логин или пароль.")

    else:
        form = None

    return render(request, 'users/profile.html', {
        'register_form': RegisterForm(),
        'login_form': LoginForm(),
        'from_page': from_page
    })

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and email_verification_token.check_token(user, token):
        profile = getattr(user, 'profile', None)
        if profile:
            profile.is_email_verified = True
            profile.save()
        messages.success(request, 'Почта подтверждена. Спасибо!')
        return redirect('profile')
    else:
        messages.error(request, 'Ссылка недействительна или устарела.')
        return redirect('profile')

@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        full_name = request.POST.get('full_name', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()

        user = request.user
        changed = False

        if email and email != user.email:
            user.email = email
            user.profile.is_email_verified = False
            user.profile.save()
            send_verification_email(request, user)
            messages.info(request, "Почта изменена — требуется повторное подтверждение.")
            changed = True

        if username and username != user.username:
            user.username = username
            changed = True

        if password:
            user.set_password(password)
            changed = True

        if changed:
            user.save()

        profile = getattr(user, 'profile', None)
        if profile:
            profile.full_name = full_name
            profile.address = address
            profile.city = city
            profile.save()

        if changed:
            messages.success(request, 'Данные успешно обновлены.')
            if password:
                from django.contrib.auth import update_session_auth_hash
                update_session_auth_hash(request, user)

        return redirect('profile')

    return render(request, 'users/profile_logged.html')

@login_required
def profile_view(request):
    from_page = request.GET.get("from", "")
    return render(request, 'users/profile_logged.html', {
        'from_page': from_page,
        'section': 'profile',
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from orders.models import Order
from booking.models import Booking

@login_required
def profile_logged(request):
    user = request.user
    profile = getattr(user, 'profile', None)
    full_name = profile.full_name if profile else ''

    print(f"[DEBUG] User email: {user.email}")
    print(f"[DEBUG] User full_name: {full_name}")

    purchases = Order.objects.filter(email=user.email).order_by('-created_at')
    print(f"[DEBUG] Purchases count: {purchases.count()}")

    bookings = Booking.objects.filter(email=user.email).order_by('-date', '-time')
    print(f"[DEBUG] Bookings count (filtered by email only): {bookings.count()}")

    return render(request, 'users/profile_logged.html', {
        'purchases': purchases,
        'bookings': bookings,
    })

