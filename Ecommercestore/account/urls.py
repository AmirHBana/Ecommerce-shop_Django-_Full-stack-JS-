from django.urls import path, reverse_lazy
from . import views

# import library for password management
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('register/', views.register, name='register'),


    # Email verification url's

    path('email-verification/<str:uidb64>/<str:token>/', views.email_verification, name='email-verification'),


    path('email-verification-sent/', views.email_verification_sent, name='email-verification-sent'),


    path('email-verification-success/', views.email_verification_success, name='email-verification-success'),


    path('email-verification-failed/', views.email_verification_failed, name='email-verification-failed'),


    # Login / Logout urls

    path('my-login/', views.my_login, name='my-login'),

    path('user-logout/', views.user_logout, name='user-logout'),

    # Dashboard url / profile urls / delete account

    path('dashboard/', views.dashboard, name='dashboard'),

    path('profile-management/', views.profile_management, name='profile-management'),

    path('delete-account/', views.delete_account, name='delete-account'),


    # password management urls/views
    # 1) submit our email form

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='account/password/password-reset.html',
        success_url=reverse_lazy('reset_password_done')),name='reset_password'),

    # 2) success massage stating that a password reset email was sent

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='account/password/password-reset-sent.html'), name='reset_password_done'),

    # 3) password reset link

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/password/password-reset-form.html'), name='password_reset_confirm'),

    # 4) success massage stating that our password was reset

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password/password-reset-complete.html'), name='password_reset_complete'),

    # Manage shipping url

    path('manage-shipping/', views.manage_shipping, name='manage-shipping'),

    # Track order
    path('track-orders/', views.track_orders, name='track-orders'),

    # Change password
    path('change-password/', views.change_password, name='change-password'),

]