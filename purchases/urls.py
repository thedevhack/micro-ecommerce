from django.urls import path
from . import views

app_name = 'purchases'
urlpatterns = [
    path('start/', views.purchase_started_view, name='start'),
    path('success/', views.purchase_success_view, name='success'),
    path('done/', views.purchase_stopped_view, name='done'),
    ]