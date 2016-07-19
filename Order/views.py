from django.shortcuts import render, redirect
from Order.models import *
from Order.forms import *
import arrow


def home(request):
    if request.GET.get('New Order') == 'New Order':
        return redirect(order_form)
    elif request.GET.get('All Orders') == 'All Orders':
        return redirect(get_orders)
    else:
        return redirect(order_form)


def order_form(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            order_datetime = arrow.utcnow()
            order = Order.objects.create(product=data.get('product'),
                                         customer=data.get('customer'),
                                         email=data.get('email'),
                                         paid_BYR=data.get('paid_BYR'),
                                         paid_BYN=data.get('paid_BYN'),
                                         comment=data.get('comment'),
                                         order_datetime=order_datetime.datetime,
                                         )
            return redirect(home)
        else:
            context = {'OrderForm': form}
            return render(request, 'order_form.html', context)

    else:
        context = {'OrderForm': OrderForm()}
        return render(request, 'order_form.html', context)


def get_orders(request):
    orders = Order.objects.filter()
    context = {'orders': orders}
    return render(request, 'get_orders.html', context)


