from django.db import models
from shop.models import Product
# 优惠码
from decimal import Decimal
from django.core.validators import MinValueValidator, \
                                    MaxValueValidator
from coupons.models import Coupon


class Order(models.Model):
    name = models.CharField(max_length=50, verbose_name='姓名')
    phone = models.CharField(max_length=11, verbose_name='手机', blank=True)
    city = models.CharField(max_length=100, verbose_name='城市')
    address = models.CharField(max_length=250, verbose_name='地址')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    email = models.EmailField()

    # payment
    pay_id = models.CharField(max_length=150, blank=True)

    # 优惠码
    coupon = models.ForeignKey(Coupon,
                                related_name='orders',
                                null=True,
                                blank=True,
                                on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0,
                                validators=[MinValueValidator(0),
                                MaxValueValidator(100)])

    class Meta:
        ordering = ('-created',)
        verbose_name = '订单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        # return sum(item.get_cost() for item in self.items.all())
        # 考虑优惠
        total_cost = sum(item.get_cost() for item in self.items.all())
        # DE8UG开头的，直接减
        # SALE开头的，打折
        # WHOS开头的，老板定
        if self.coupon.code.startswith('SALE'):
            return total_cost - total_cost * (self.discount / Decimal('100'))
        elif self.coupon.code.startswith('DE8UG'):
            return total_cost - self.discount
        elif self.coupon.code.startswith('WHOS'):
            return 1
        else:
            return total_cost


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    quantity = models.PositiveIntegerField(default=1, verbose_name='数量')

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
