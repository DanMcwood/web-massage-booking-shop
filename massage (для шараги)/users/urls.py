from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    profile_auth_view,
    profile_edit_view,
    profile_view,
    verify_email,
)

urlpatterns = [
    path('', profile_auth_view, name='profile'),
    path('edit/', profile_edit_view, name='profile_edit'),
    path('verify-email/<uidb64>/<token>/', verify_email, name='verify_email'),

    path('logout/', auth_views.LogoutView.as_view(next_page='/profile/'), name='logout'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]
