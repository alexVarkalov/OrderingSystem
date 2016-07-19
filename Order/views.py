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
        time = arrow.utcnow().time()
        time = time.replace(hour=14)
        start_time = arrow.get(46800).time()
        end_time = arrow.get(54000).time()
        if time > end_time or time < start_time:
            permission = False
        else:
            permission = True
        context = {'OrderForm': OrderForm(),
                   'permission': permission
                   }
        return render(request, 'order_form.html', context)


def get_orders(request):
    orders = Order.objects.filter()
    BYN_sum = 0
    BYR_sum = 0
    for order in orders:
        if order.paid_BYN:
            BYN_sum += order.paid_BYN
        elif order.paid_BYR:
            BYR_sum += order.paid_BYR
    result_BYN = BYN_sum + float(BYR_sum)/10000
    context = {'orders': orders,
               'BYN_sum': BYN_sum,
               'BYR_sum': BYR_sum,
               'result_BYN': result_BYN
               }
    return render(request, 'get_orders.html', context)


