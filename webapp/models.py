from django.db import models
from adminApp.models import User, Cake

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE)
    qty = models.PositiveSmallIntegerField(default=1)
    total_price = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cart'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sub_total = models.FloatField(default=0)
    delivery_charge = models.FloatField(default=0)
    discount = models.PositiveSmallIntegerField(default=0)
    order_total = models.FloatField(default=0)
    order_id = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'

class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE)
    qty = models.PositiveSmallIntegerField(default=1)
    total_price = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'order_details'