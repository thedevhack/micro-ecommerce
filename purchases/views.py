import random
import stripe
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse
from products.models import Product
from .models import Purchase

from microEcommerce.env import config

STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY', default=None)
stripe.api_key = STRIPE_SECRET_KEY

STRIPE_BASE_ENDPOINT = 'http://127.0.0.1:8000'

def purchase_started_view(request):
    if not request.method == "POST" or not request.user.is_authenticated:
        return HttpResponseBadRequest()
    handle = request.POST.get('handle')
    obj = Product.objects.get(handle=handle)
    stripe_price_id = obj.stripe_price_id
    if stripe_price_id is None:
        return HttpResponseBadRequest()
    purchase = Purchase.objects.create(user=request.user, product=obj)
    request.session['purchase_id'] = purchase.id
    success_path = reverse('purchases:success')
    cancel_path = reverse('purchases:done')

    if not success_path.startswith('/'):
        success_path = f"/{success_path}"
    success_url = f"{STRIPE_BASE_ENDPOINT}/{success_path}"
    cancel_url = f"{STRIPE_BASE_ENDPOINT}/{cancel_path}"
    checkout_session = stripe.checkout.Session.create(
        line_items = [
            {
                "price":stripe_price_id,
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url
    )
    purchase.stripe_checkout_session_id = checkout_session.id
    purchase.save()
    return HttpResponseRedirect(checkout_session.url)


def purchase_success_view(request):
    purchase_id = request.session.get('purchase_id')
    if purchase_id:
        purchase = Purchase.objects.get(id = purchase_id)
        purchase.is_completed = True
        purchase.save()
        del request.session['purchase_id']
        return HttpResponseRedirect(purchase.product.get_absolute_url())
    return HttpResponse(f'finished {purchase_id}')


def purchase_stopped_view(request):
    purchase_id = request.session.get('purchase_id')
    if purchase_id:
        purchase = Purchase.objects.get(id=purchase_id)
        product = purchase.product
        del request.session['purchase_id']
        return HttpResponseRedirect(product.get_absolute_url())
    return HttpResponse('Stopped')