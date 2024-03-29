from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
import pathlib
import stripe
from microEcommerce.env import config

STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY', default=None)
stripe.api_key = STRIPE_SECRET_KEY

PROTECTED_MEDIA_ROOT = settings.PROTECTED_MEDIA_ROOT
protected_storage = FileSystemStorage(location=str(PROTECTED_MEDIA_ROOT))

class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default= 1, on_delete=models.CASCADE)
    stripe_product_id = models.CharField(max_length=220, blank=True, null=True)
    name = models.CharField(max_length=120)
    handle = models.SlugField(unique=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=9.99)
    og_price = models.DecimalField(max_digits=10, decimal_places=2, default=9.99)
    stripe_price = models.IntegerField(default=999)
    stripe_price_id = models.CharField(max_length=220, blank=True, null=True)
    price_changed_timestamp = models.DateTimeField(auto_now=False,
                                                       auto_now_add=False, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.name}'


    def save(self, *args, **kwargs):
        if self.name:
            stripe_product_response = stripe.Product.create(name=self.name)
            self.stripe_product_id = stripe_product_response.id
        if not self.stripe_price_id:
            stripe_price_obj = stripe.Price.create(
                product=self.stripe_product_id,
                unit_amount=self.stripe_price,
                currency="inr",
            )
            self.stripe_price_id = stripe_price_obj.id
        if self.price != self.og_price:
            # -> price changed
            self.og_price = self.price
            # -> trigger an API request for the price
            self.stripe_price = int(self.price * 100)
            if self.stripe_product_id:
                stripe_price_obj = stripe.Price.create(
                    product=self.stripe_product_id,
                    unit_amount=self.stripe_price,
                    currency="inr"
                )
                self.stripe_price_id = stripe_price_obj.id
            self.price_changed_timestamp = timezone.now()
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('products:detail', kwargs={
            'handle': self.handle
        })

    def get_manage_url(self):
        return reverse('products:manage', kwargs={
            'handle': self.handle
        })


    @property
    def get_display_price(self):
        return self.price

def handle_product_attachment_upload(instance, filename):
    return f'products/{instance.product.handle}/attachments/{filename}'


class ProductAttachment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file = models.FileField(upload_to=handle_product_attachment_upload, storage=protected_storage)
    name = models.CharField(max_length=120, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    is_free = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = pathlib.Path(self.file.name).name
        super().save(*args, **kwargs)

    @property
    def display_name(self):
        return self.name or pathlib.Path(self.file.name).name

    def get_download_url(self):
        return reverse('products:attachment_download', kwargs={
            'handle': self.product.handle,
            'pk': self.pk
        })