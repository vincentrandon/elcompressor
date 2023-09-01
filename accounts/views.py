from datetime import datetime

import stripe
from django.contrib import auth, messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt

from accounts.forms import UserEditForm, EditUserPasswordForm, GenerateApiKeyForm, ResetPasswordForm
from accounts.helpers import send_mail_sendinblue
from accounts.models import User, StripeCustomer, UserAPIKey
from config import settings
from tool.models import ImageUpload


# Create your views here.
def login_user(request: HttpRequest) -> render:
    # Login the user
    if request.user.is_authenticated:
        return redirect('tool:index')
    else:
        if request.method == 'POST':
            username = request.POST['email']
            print(username)
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect('tool:index')
            else:
                messages.info(request, ('Invalid Username or Password'))
                return render(request, 'registration/login.html')
        else:
            return render(request, 'registration/login.html')


def signup_user(request: HttpRequest) -> render:
    # Signup the user
    if request.user.is_authenticated:
        return redirect('tool:index')
    else:
        if request.method == 'POST':
            email_address = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']
            if password == password2:
                if User.objects.filter(email=email_address).exists():
                    messages.info(request, ('Email is already taken'))
                    return render(request, 'registration/signup.html')
                else:
                    user = User.objects.create_user(email=email_address, password=password, username=email_address)
                    user.credits = 100
                    user.save()
                    messages.success(request, ("You've successfully created an account"))
                    send_mail_sendinblue(
                        template_id=1,
                        to=str(email_address),
                        params={'email': str(email_address)}
                    )
                    return redirect('accounts:login')
            else:
                messages.info(request, ('Passwords do not match'))
                return render(request, 'registration/signup.html')
        else:
            return render(request, 'registration/signup.html')


@login_required
def logout_user(request: HttpRequest) -> render:
    # Logout the user
    auth.logout(request)
    messages.info(request, ('You have been logged out'))
    return redirect('accounts:login')


def forgot_password(request: HttpRequest) -> render:
    form = ResetPasswordForm()
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            password = get_random_string(length=10)
            user.set_password(password)
            user.save()
            mail = send_mail_sendinblue(
                template_id=2,
                to=str(email),
                email=email,
                password=password
            )
            messages.success(request, ("Your password has been reset. Please check your email."))
            return redirect('accounts:login')
        else:
            print(form.errors)
            messages.error(request, (form.errors))
    return render(request, 'registration/forgot-password.html', context={'form': form})


@login_required
def display_profile(request: HttpRequest) -> render:
    user = request.user
    initial = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    }
    form = UserEditForm(initial=initial)
    nb_images = ImageUpload.objects.filter(user=user).count()
    return render(request, 'profile/profile.html', context={'user': user, 'form': form, 'nb_images': nb_images})


@login_required
def edit_profile(request: HttpRequest):
    user = request.user
    form = UserEditForm(instance=user)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return render(request, 'profile/partials/partial-edit-user.html',
                          context={'user': user, 'form': form})
    return render(request, 'profile/partials/partial-edit-user.html',
                  context={'user': user, 'form': form})

@login_required
def security_zone(request: HttpRequest) -> render:
    user = request.user
    form = EditUserPasswordForm(user=user)
    user_api_key = UserAPIKey.objects.filter(user=user)
    return render(request, 'profile/security.html', context={'user': user, 'form': form, 'user_api_key': user_api_key})

@login_required
def edit_password(request: HttpRequest) -> render:
    user = request.user
    form = EditUserPasswordForm(user=user)
    if request.method == 'POST':
        form = EditUserPasswordForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'profile/partials/partial-edit-password.html', context={'user': user, 'form': form})
        else:
            print(form.errors)
            messages.error(request, (form.errors))

    return render(request, 'profile/partials/partial-edit-password.html', context={'user': user, 'form': form})

@login_required
def generate_api_key(request: HttpRequest) -> render:
    user = request.user
    form = GenerateApiKeyForm()
    if request.method == 'POST':
        print(request.POST)
        form = GenerateApiKeyForm(request.POST)
        print(form)
        if form.is_valid():
            UserAPIKey.objects.create_key(name=request.user.username, user=user)
            return render(request, 'profile/partials/partial-generate-api-key.html',
                          context={'user': user, 'form': form})
        else:
            print(form.errors)
            messages.error(request, (form.errors))

    return render(request, 'profile/partials/partial-generate-api-key.html', context={'user': user})

@login_required
def delete_account(request: HttpRequest) -> render:
    user = request.user
    if request.method == 'POST':
        user.delete()
        messages.info(request, ('Your account has been deleted'))
        return redirect('accounts:login')

    return render(request, 'profile/partials/partial-delete-account.html', context={'user': user})

@login_required
def history_images(request: HttpRequest) -> render:
    user = request.user
    images = ImageUpload.objects.filter(user=user).order_by('-date')
    return render(request, 'profile/history.html', context={'user': user, 'images': images}
                  )

@login_required
def plans(request: HttpRequest) -> render:
    user = request.user
    suscribed_user = StripeCustomer.objects.get(user=user)
    return render(request, 'profile/plans.html', context={'user': user, 'suscribed_user': suscribed_user})

@login_required
def billing(request: HttpRequest) -> render:
    user = request.user
    stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
    # We get the stripe customer object
    stripe_customer = StripeCustomer.objects.get(user=user)
    # We get invoices related to the customer
    invoices = stripe.Invoice.list(customer=stripe_customer.stripe_customer_id)

    return render(request, 'profile/billing.html', context={'user': user, 'invoices': invoices})


@csrf_exempt
def stripe_config(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_TEST_PUBLIC_KEY}
        print('stripe_config: ', stripe_config)
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        domain_url = 'http://127.0.0.1:8000/'
        stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url + 'accounts/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'accounts/cancel/',
                payment_method_types=['card'],
                mode='subscription',
                customer_email=request.user.email if request.user.is_authenticated else None,
                line_items=[
                    {
                        'price': settings.STRIPE_PRICE_ID,
                        'quantity': 1,
                    }
                ]
            )
            print(checkout_session)
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


def success(request: HttpRequest) -> render:
    user = request.user
    return render(request, 'profile/success.html', context={'user': user})


def cancel(request: HttpRequest) -> render:
    user = request.user
    return render(request, 'profile/cancel.html', context={'user': user})


@csrf_exempt
def stripe_webhook(request: HttpRequest) -> HttpResponse:
    stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Fetch all the required data from session
        client_reference_id = session.get('client_reference_id')
        stripe_customer_id = session.get('customer')
        stripe_subscription_id = session.get('subscription')
        # We get the subscription object to get the start and end date
        subscription = stripe.Subscription.retrieve(stripe_subscription_id)
        subscription_start_date = datetime.utcfromtimestamp(subscription['current_period_start'])
        subscription_end_date = datetime.utcfromtimestamp(subscription['current_period_end'])

        # Get the user and create a new StripeCustomer if doesn't exist else update the existing one
        user = User.objects.get(id=client_reference_id)
        stripe_customer, created = StripeCustomer.objects.get_or_create(user=user)
        print(f'Stripe customer is {stripe_customer}')
        stripe_customer.stripe_customer_id = stripe_customer_id
        stripe_customer.stripe_subscription_id = stripe_subscription_id
        stripe_customer.stripe_subscription_status = True
        stripe_customer.subscription_cancelled = False
        stripe_customer.subscription_beginning_date = subscription_start_date
        stripe_customer.subscription_ending_date = subscription_end_date
        stripe_customer.subscription_cancelled_date = None
        stripe_customer.save()

    return HttpResponse(status=200)


@csrf_exempt
def cancel_subscription(request: HttpRequest) -> JsonResponse:
    print('cancel_subscription')
    if request.method == 'GET':
        stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
        user = request.user
        stripe_customer = StripeCustomer.objects.get(user=user)
        stripe_subscription_id = stripe_customer.stripe_subscription_id
        subscription = stripe.Subscription.retrieve(stripe_subscription_id)
        print(subscription)
        subscription.delete()
        stripe_customer.subscription_cancelled = True
        stripe_customer.subscription_cancelled_date = datetime.utcfromtimestamp(subscription['canceled_at'])
        stripe_customer.save()
        return JsonResponse({'status': 'Subscription cancelled.'})
