from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from home import views as home_views

urlpatterns = [
    path('', home_views.home, name='home'),
    path('admin/', admin.site.urls),
    path('home/', include('home.urls')),
    path('booking/', include('booking.urls')),
    path('services/', include('services.urls')),
    path('store/', include('store.urls')),
    path('profile/', include('users.urls')),
    path('order/', include('orders.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
