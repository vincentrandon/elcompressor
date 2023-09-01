from django.contrib import admin

from accounts.models import User, StripeCustomer, UserAPIKey


# Register your models here.
class UserAdmin(admin.ModelAdmin):

    list_display = ['email', 'first_name', 'last_name', 'date_joined', 'is_active', 'is_staff', 'is_superuser']
    model = User

admin.site.register(User, UserAdmin)


class CustomUserApiKeyAdmin(admin.ModelAdmin):

        list_display = ['user', 'hashed_key']
        model = UserAPIKey

admin.site.register(UserAPIKey, CustomUserApiKeyAdmin)


class StripeCustomerAdmin(admin.ModelAdmin):

        list_display = ['user', 'stripe_customer_id', 'stripe_subscription_id', 'stripe_subscription_status']
        model = StripeCustomer

admin.site.register(StripeCustomer, StripeCustomerAdmin)