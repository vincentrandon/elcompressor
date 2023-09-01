from django.urls import path

from accounts.views import login_user, display_profile, edit_profile, logout_user, security_zone, edit_password, \
    delete_account, history_images, plans, billing, stripe_config, create_checkout_session, success, cancel, \
    stripe_webhook, cancel_subscription, signup_user, generate_api_key, forgot_password

app_name = 'accounts'

urlpatterns = [
    path('login', login_user, name='login'),
    path('signup', signup_user, name='signup'),
    path('forgot-password', forgot_password, name='forgot-password'),
    path('profile', display_profile, name='profile'),
    path('edit-profile', edit_profile, name='edit-profile'),
    path('logout', logout_user, name='logout'),
    path('security', security_zone, name='security'),
    path('edit-password', edit_password, name='edit-password'),
    path('delete-account', delete_account, name='delete-account'),
    path('history', history_images, name='history-images'),
    path('plans', plans, name='plans'),
    path('billing', billing, name='billing'),
    path('payment', stripe_config, name='payment'),
    path('create-checkout-session', create_checkout_session, name='create-checkout-session'),
    path('success', success, name='success'),
    path('cancel', cancel, name='cancel'),
    path('webhook', stripe_webhook, name='webhook'),
    path('cancel-subscription', cancel_subscription, name='cancel-subscription'),
    path('generate-api-key', generate_api_key, name='generate-api-key')
]