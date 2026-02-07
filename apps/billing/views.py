import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Subscription

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def subscribe(request):
    return render(request, "billing/subscribe.html")

@login_required
def create_checkout(request):
    if not settings.STRIPE_PRICE_ID:
        return redirect("subscribe")

    session = stripe.checkout.Session.create(
        mode="subscription",
        line_items=[{"price": settings.STRIPE_PRICE_ID, "quantity": 1}],
        success_url=f"{settings.SITE_URL}/billing/success/",
        cancel_url=f"{settings.SITE_URL}/billing/cancel/",
        customer_email=request.user.email or None,
    )
    return redirect(session.url, code=303)

@login_required
def success(request):
    # We'll rely on webhook to flip status to active.
    Subscription.objects.get_or_create(parent=request.user)
    return render(request, "billing/subscribe.html", {"message": "Payment received. If access doesn’t unlock in 1 minute, refresh."})

@login_required
def cancel(request):
    return render(request, "billing/subscribe.html", {"message": "Checkout cancelled."})

