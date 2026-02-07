from django.urls import path
from django.http import HttpResponse

def billing_home(request):
    return HttpResponse("Billing app is working")

urlpatterns = [
    path("", billing_home, name="billing-home"),
]
