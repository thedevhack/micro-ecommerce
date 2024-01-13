from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from .models import Product, ProductAttachment

# input_css_class = "form-control"


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'handle', 'price']

    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['name'].widget.attrs['placeholder'] = 'Your Name'
        for field in self.fields:
            self.fields['name'].widget.attrs['placeholder'] = 'Please Enter Your ' + str(field)


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'handle', 'price']

    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['name'].widget.attrs['placeholder'] = 'Your Name'
        for field in self.fields:
            self.fields['name'].widget.attrs['placeholder'] = 'Please Enter Your ' + str(field)


class ProductAttachmentForm(forms.ModelForm):
    class Meta:
        model = ProductAttachment
        fields = ['file', 'name', 'is_free', 'active']

    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['name'].widget.attrs['placeholder'] = 'Your Name'
        for field in self.fields:
            if field in ['is_free', 'active']:
                continue
            self.fields[field].widget.attrs['placeholder'] = 'Please Enter Your ' + str(field)


ProductAttachmentModelFormset = modelformset_factory(
    ProductAttachment,
    fields=['file', 'name', 'is_free', 'active'],
    extra=0,
    can_delete=True
)


ProductAttachmentInlineFormset = inlineformset_factory(
    Product,
    ProductAttachment,
    formset=ProductAttachmentModelFormset,
    fields=['file', 'name', 'is_free', 'active'],
    extra=0,
    can_delete=True
)

