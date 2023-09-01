from accounts.models import StripeCustomer


def subscribed_user(request):
    if request.user.is_authenticated:
        if not StripeCustomer.objects.filter(user=request.user).exists():
            global_subscribed_user = StripeCustomer.objects.create(user=request.user)
        else:
            global_subscribed_user = StripeCustomer.objects.get(user=request.user)
        return {'global_subscribed_user': global_subscribed_user}
    else:
        return {}