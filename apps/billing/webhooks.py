import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Subscription

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except Exception:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        email = session.get("customer_details", {}).get("email") or session.get("customer_email")
        if email:
            user = User.objects.filter(email=email).first()
            if user:
                sub, _ = Subscription.objects.get_or_create(parent=user)
                sub.stripe_customer_id = session.get("customer", "") or ""
                sub.status = "active"
                sub.save()

    if event["type"] in ("customer.subscription.deleted", "invoice.payment_failed"):
        obj = event["data"]["object"]
        customer_id = obj.get("customer")
        sub = Subscription.objects.filter(stripe_customer_id=customer_id).first()
        if sub:
            sub.status = "inactive"
            sub.save()

    return HttpResponse(status=200)
