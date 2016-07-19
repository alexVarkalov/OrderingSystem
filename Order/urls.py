from django.conf.urls import url
from Order.views import *


urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^order_form/$', order_form, name='order_form'),
    url(r'^get_orders/$', get_orders, name='get_orders'),
]