from django.test import TestCase
from Order.models import *
from django.contrib.auth.models import User
from mock import patch
from django.http import HttpResponse
import json
import arrow


def new_render(a, b, c):
    result = json.dumps(c['result_BYN'])
    return HttpResponse(result)


class TestOrder(TestCase):
    def test_ok_save_order(self):
        data = {'product': 'Dish of a Day',
                'customer': 'Alex Varkalov',
                'email': 'alex.varkalov@gmail.com',
                'paid_BYR': 50000,
                'paid_BYN': 2.5,
                'comment': 'Without Tomato',
                'Finish': 'Finish'
                }
        response = self.client.post('/orders/order_form/', data)
        status_code = response.status_code
        self.assertEquals(status_code, 302)
        orders = Order.objects.filter()
        self.assertEquals(orders.count(), 1)
        order = orders.get()
        self.assertEquals(order.product, data['product'])
        self.assertEquals(order.customer, data['customer'])
        self.assertEquals(order.email, data['email'])
        self.assertEquals(order.paid_BYR, data['paid_BYR'])
        self.assertEquals(order.paid_BYN, data['paid_BYN'])
        self.assertEquals(order.comment, data['comment'])

    def test_ok_edit_order(self):
        data1 = {'product': 'Dish of a Day',
                 'customer': 'Alex Varkalov',
                 'email': 'alex.varkalov@gmail.com',
                 'paid_BYR': 50000,
                 'paid_BYN': 2.5,
                 'comment': 'Without Tomato',
                 'Finish': 'Finish'
                 }
        data2 = {'product': 'Fish of a Day',
                 'customer': 'Alexander Varkalov',
                 'email': 'alex.varkalov@gmail.com',
                 'paid_BYR': 150000,
                 'paid_BYN': 25,
                 'comment': 'Without Tomato and Salt',
                 'Finish': 'Finish'
                 }
        User.objects.create_user(username='test', password='test', is_staff=True)
        self.client.login(username='test', password='test')
        order_datetime = arrow.utcnow()
        collective_order = CollectiveOrder.objects.create(collective_order_datetime=order_datetime.datetime)
        order = Order.objects.create(product=data1['product'],
                                     customer=data1['customer'],
                                     email=data1['email'],
                                     paid_BYR=data1['paid_BYR'],
                                     paid_BYN=data1['paid_BYN'],
                                     comment=data1['comment'],
                                     order_datetime=order_datetime.datetime,
                                     collective_order=collective_order
                                     )
        response = self.client.post('/orders/edit_order/id={0}'.format(order.id), data2)
        status_code = response.status_code
        self.assertEquals(status_code, 302)
        edited_orders = Order.objects.filter()
        self.assertEquals(edited_orders.count(), 1)
        edited_order = edited_orders.get()
        self.assertEquals(edited_order.product, data2['product'])
        self.assertEquals(edited_order.customer, data2['customer'])
        self.assertEquals(edited_order.email, data2['email'])
        self.assertEquals(edited_order.paid_BYR, data2['paid_BYR'])
        self.assertEquals(edited_order.paid_BYN, data2['paid_BYN'])
        self.assertEquals(edited_order.comment, data2['comment'])

    def test_ok_delete(self):
        User.objects.create_user(username='test', password='test', is_staff=True)
        self.client.login(username='test', password='test')
        data = {'product': 'Dish of a Day',
                'customer': 'Alex Varkalov',
                'email': 'alex.varkalov@gmail.com',
                'paid_BYR': 50000,
                'paid_BYN': 2.5,
                'comment': 'Without Tomato',
                'Finish': 'Finish'
                }
        order_datetime = arrow.utcnow()
        collective_order = CollectiveOrder.objects.create(collective_order_datetime=order_datetime.datetime)
        order = Order.objects.create(product=data['product'],
                                     customer=data['customer'],
                                     email=data['email'],
                                     paid_BYR=data['paid_BYR'],
                                     paid_BYN=data['paid_BYN'],
                                     comment=data['comment'],
                                     order_datetime=order_datetime.datetime,
                                     collective_order=collective_order
                                     )
        orders = Order.objects.filter()
        self.assertEquals(orders.count(), 1)
        response = self.client.post('/orders/delete_order/id={0}'.format(order.id))
        status_code = response.status_code
        self.assertEquals(status_code, 302)
        orders = Order.objects.filter()
        self.assertEquals(orders.count(), 0)

    def test_ok_sum(self):
        with patch('Order.views.render', new=new_render):
            User.objects.create_user(username='test', password='test', is_staff=True)
            self.client.login(username='test', password='test')
            data1 = {'product': 'Dish of a Day',
                     'customer': 'Alex Varkalov',
                     'email': 'alex.varkalov@gmail.com',
                     'paid_BYR': 50000,
                     'paid_BYN': 2.5,
                     'comment': 'Without Tomato',
                     'Finish': 'Finish'
                     }
            data2 = {'product': 'Fish of a Day',
                     'customer': 'Alexander Varkalov',
                     'email': 'alex.varkalov@gmail.com',
                     'paid_BYR': 150000,
                     'paid_BYN': 25,
                     'comment': 'Without Tomato and Salt',
                     'Finish': 'Finish'
                     }
            order_datetime = arrow.utcnow()
            collective_order = CollectiveOrder.objects.create(collective_order_datetime=order_datetime.datetime)
            order1 = Order.objects.create(product=data1['product'],
                                          customer=data1['customer'],
                                          email=data1['email'],
                                          paid_BYR=data1['paid_BYR'],
                                          paid_BYN=data1['paid_BYN'],
                                          comment=data1['comment'],
                                          order_datetime=order_datetime.datetime,
                                          collective_order=collective_order
                                          )
            order2 = Order.objects.create(product=data2['product'],
                                          customer=data2['customer'],
                                          email=data2['email'],
                                          paid_BYR=data2['paid_BYR'],
                                          paid_BYN=data2['paid_BYN'],
                                          comment=data2['comment'],
                                          order_datetime=order_datetime.datetime,
                                          collective_order=collective_order
                                          )
            BYN_sum = 0
            BYR_sum = 0
            orders = [order1, order2]
            for order in orders:
                if order.paid_BYN:
                    BYN_sum += order.paid_BYN
                if order.paid_BYR:
                    BYR_sum += order.paid_BYR
            result_BYN = BYN_sum + float(BYR_sum) / 10000
            result = self.client.post('/orders/get_collective_order/id={}'.format(collective_order.id))
            content = json.loads(result.content)
            status_code = result.status_code
            self.assertEquals(status_code, 200)
            self.assertEquals(result_BYN, content)
