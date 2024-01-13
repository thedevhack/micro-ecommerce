from django.db import models
from django.conf import settings
from products.models import Product


class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    is_completed = models.BooleanField(default=False)
    stripe_price = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    stripe_checkout_session_id = models.CharField(max_length=220, null=True, blank=True)