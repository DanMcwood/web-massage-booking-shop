from django.urls import path
from .views import booking, thanks

urlpatterns = [
    path('', booking, name='booking'),
    path('thanks/', thanks, name='thanks'),
]
