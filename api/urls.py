from django.contrib import admin
from django.urls import path, re_path
from .views import get_create_order, payment_charge_api, index_page

urlpatterns = [
  path('', index_page, name='home'),
  path('price-detail/', get_create_order, name='create_order'),
  path('order-charge/<order_id>/<request_id>/', payment_charge_api, name='order_charge'),
]
