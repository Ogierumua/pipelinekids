import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .utils import get_or_create_subscription

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def pricing(request):
    return render(request, "billing/pricing.html")


@login_required
def create_checkout_session(request):
    subscription = get_or_create_subscription(request.user)

    checkout_session = stripe.checkout.Session.create(
        customer=subscription.stripe_customer_id or None,
        mode="subscription",
        line_items=[{
            "price": settings.STRIPE_PRICE_ID_MONTHLY,
            "quantity": 1,
        }],
        success_url=settings.SITE_URL + "/billing/success/",
        cancel_url=settings.SITE_URL + "/billing/cancel/",
    )

    return redirect(checkout_session.url, code=303)


# Backward-compatible alias (optional)
create_checkout = create_checkout_session


@login_required
def billing_success(request):
    return render(request, "billing/success.html")


@login_required
def billing_cancel(request):
    return render(request, "billing/cancel.html")
