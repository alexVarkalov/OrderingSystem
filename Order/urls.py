from django.conf.urls import url
from Order.views import *

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^order_form/$', order_form, name='order_form'),
    url(r'^get_orders/$', get_orders, name='get_orders'),
    url(r'^get_collective_orders/$', get_collective_orders, name='get_collective_orders'),
    url(r'^get_collective_order/id=(?P<collective_order_id>[0-9]+)$',
        get_collective_order, name='get_collective_order'),
    url(r'^edit_order/id=(?P<order_id>[0-9]+)$', edit_order, name='edit_order'),
    url(r'^delete_order/id=(?P<order_id>[0-9]+)$', delete_order, name='delete_order'),
    url(r'^delete_collective_order/id=(?P<collective_order_id>[0-9]+)$',
        delete_collective_order, name='delete_collective_order'),
]
