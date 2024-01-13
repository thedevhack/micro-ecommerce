from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest, FileResponse
import mimetypes
from .models import Product, ProductAttachment
from .forms import ProductForm, ProductUpdateForm, ProductAttachmentInlineFormset


def product_create_view(request):
    context = {}
    form = ProductForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        if request.user.is_authenticated:
            obj.user = request.user
            obj.save()
            return redirect(obj.get_manage_url())
        form.add_error(None, "You must be logged in to create products")


    context["form"] = form
    return render(request, "products/create.html", context)


def product_list_view(request):
    context = {"products":Product.objects.all()}
    print(context)
    return render(request, 'products/list.html', context)


def product_manage_detail_view(request, handle=None):
    obj = get_object_or_404(Product, handle=handle)
    attachments = ProductAttachment.objects.filter(product=obj)
    is_manager = request.user == obj.user
    context = {"object": obj}
    if not is_manager:
        return HttpResponseBadRequest()
    form = ProductUpdateForm(request.POST or None, request.FILES or None, instance=obj)
    formset = ProductAttachmentInlineFormset(request.POST or None,
                                             request.FILES or None,
                                             queryset=attachments)
    if form.is_valid() and formset.is_valid():
        instance = form.save(commit=False)
        instance.save()
        formset.save(commit=False)
        for _form in formset:
            is_delete = _form.cleaned_data.get("DELETE")
            try:
                attachment_obj = _form.save(commit=False)
            except:
                attachment_obj = None
            if is_delete:
                if attachment_obj:
                    if attachment_obj.pk:
                        attachment_obj.delete()
            else:
                if attachment_obj:
                    attachment_obj.product = instance
                    attachment_obj.save()
        return redirect(obj.get_manage_url())
        # return redirect('/products/create/')
    # form.add_error(None, "You must be logged in to create products")
    context["form"] = form
    context['formset'] = formset
    return render(request, "products/manager.html", context)


def product_detail_view(request, handle=None):
    obj = get_object_or_404(Product, handle=handle)
    attachments = ProductAttachment.objects.filter(product=obj)
    is_owner = False
    if request.user.is_authenticated:
        is_owner = request.user.purchase_set.all().filter(product=obj, is_completed=True).exists()  # verify ownership
    context = {"object": obj, "is_owner": is_owner, "attachments":attachments}
    return render(request, "products/detail.html", context)


def product_attachment_download_view(request, handle=None, pk=None):
    attachment = get_object_or_404(ProductAttachment,
                                   product__handle=handle, pk=pk)
    can_download = attachment.is_free or False
    if request.user.is_authenticated:
        can_download = True  # check ownership
    if can_download is False:
        return HttpResponseBadRequest()
    file = attachment.file.open(mode='rb')  # cdn -> S$ object storage
    filename = attachment.file.name
    content_type, _ = mimetypes.guess_type(filename)
    response = FileResponse(file)
    response['Content-Type'] = content_type or 'application/octet-stream'
    response['Content-Disposition'] = f'attachment;filename={filename}'
    return response
