from django.contrib import admin
from django.urls import path, re_path
from .views import send_json, get_create_order, payment_charge_api, index_page

urlpatterns = [
  path('', index_page, name='home'),
  path('test/', send_json, name='test'),
  path('price-detail/', get_create_order, name='create_order'),
  # re_path('order-charge/', payment_charge_api, name='order_charge'),
  # re_path(r'^order-charge/(?P<order_id>)/$', payment_charge_api, name='order_charge'),
  path('order-charge', payment_charge_api, name='order_charge'),
]
