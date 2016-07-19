from __future__ import unicode_literals

from django.db import models


class CollectiveOrder(models.Model):
    collective_order_datetime = models.DateTimeField()


class Order(models.Model):
    product = models.CharField(max_length=30)
    customer = models.CharField(max_length=40)
    email = models.EmailField()
    paid_BYR = models.IntegerField(null=True, )
    paid_BYN = models.FloatField(null=True)
    comment = models.CharField(max_length=300, null=True)
    order_datetime = models.DateTimeField()
    collective_order = models.ForeignKey(CollectiveOrder, default=None)
