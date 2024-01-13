from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('create/', views.product_create_view, name='create'),
    path('list/', views.product_list_view, name='list'),
    path('<slug:handle>/', views.product_detail_view, name='detail'),
    path('<slug:handle>/manage/', views.product_manage_detail_view, name='manage'),
    path('<slug:handle>/download/<int:pk>', views.product_attachment_download_view, name='attachment_download'),
]