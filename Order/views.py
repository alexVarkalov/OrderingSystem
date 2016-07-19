from django.shortcuts import render, redirect
from Order.models import *
from Order.forms import *
import arrow


def home(request):
    if request.GET.get('New Collect Order') == 'New Collect Order':
        if request.session.has_key('collective_order_id'):
            del request.session['collective_order_id']
        return redirect(order_form)
    elif request.GET.get('All Collect Orders') == 'All Collect Orders':
        return redirect(get_collective_orders)
    else:
        context = {}
        return render(request, 'home.html', context)


def order_form(request):
    if request.GET.get('All Right') == 'All Right':
        del request.session['collective_order_id']
        return redirect(home)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            order_datetime = arrow.utcnow()
            if request.session.has_key('collective_order_id'):
                collective_order_id = request.session.get('collective_order_id')
                collective_order = CollectiveOrder.objects.filter(id=collective_order_id).get()
            else:
                collective_order = CollectiveOrder.objects.create(collective_order_datetime=order_datetime.datetime)
                request.session['collective_order_id'] = collective_order.id
            Order.objects.create(product=data.get('product'),
                                 customer=data.get('customer'),
                                 email=data.get('email'),
                                 paid_BYR=data.get('paid_BYR'),
                                 paid_BYN=data.get('paid_BYN'),
                                 comment=data.get('comment'),
                                 order_datetime=order_datetime.datetime,
                                 collective_order=collective_order,
                                 )
            if request.POST.get('New Order') == 'New Order':
                return redirect(order_form)
            elif request.POST.get('Finish') == 'Finish':
                return redirect(get_orders)
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
    collective_order_id = request.session.get('collective_order_id')
    orders = Order.objects.filter(collective_order__id=collective_order_id)
    BYN_sum = 0
    BYR_sum = 0
    for order in orders:
        if order.paid_BYN:
            BYN_sum += order.paid_BYN
        elif order.paid_BYR:
            BYR_sum += order.paid_BYR
    result_BYN = BYN_sum + float(BYR_sum) / 10000
    context = {'orders': orders,
               'BYN_sum': BYN_sum,
               'BYR_sum': BYR_sum,
               'result_BYN': result_BYN
               }
    return render(request, 'get_orders.html', context)


# ADMIN


def get_collective_orders(request):
    collective_orders = CollectiveOrder.objects.filter()
    context = {'collective_orders': collective_orders}
    return render(request, 'get_collecive_orders.html', context)


def get_collective_order(request, collective_order_id):
    orders = Order.objects.filter(collective_order__id=collective_order_id)
    BYN_sum = 0
    BYR_sum = 0
    for order in orders:
        if order.paid_BYN:
            BYN_sum += order.paid_BYN
        elif order.paid_BYR:
            BYR_sum += order.paid_BYR
    result_BYN = BYN_sum + float(BYR_sum) / 10000
    context = {'orders': orders,
               'BYN_sum': BYN_sum,
               'BYR_sum': BYR_sum,
               'result_BYN': result_BYN
               }
    return render(request, 'get_orders_admin.html', context)


def edit_order(request, order_id):
    return redirect(get_collective_orders)


def delete_order(request, order_id):
    return redirect(get_collective_orders)


def delete_collective_order(request, collective_order_id):
    orders = Order.objects.filter(collective_order__id=collective_order_id)
    collective_order = CollectiveOrder.objects.filter(id=collective_order_id)
    for order in orders:
        order.delete()
    collective_order.delete()
    return redirect(get_collective_orders)
