from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupons.models import Coupon


class Cart:

    def __init__(self, request):
        """
        初始化购物车对象
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

        # 优惠券
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, quantity=1, update_quantity=False):
        """
        添加商品到购物车，并更新数量
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                      'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # 告诉django，session已经被修改
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def __iter__(self):
        """
        从数据库迭代取出购物车中的商品信息
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    
    def __len__(self):
        """
        计算购物车中所有商品的个数，即总长度
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    # 优惠券
    @property
    def coupon(self):
        # 获取优惠券对象
        if self.coupon_id:
            obj = Coupon.objects.get(id=self.coupon_id)
            if obj.active:
                return obj
        return None
    
    def get_discount(self):
        # 获取打折价格
        if self.coupon:
            if self.coupon.code.startswith('SALE'):
                return (self.coupon.discount / Decimal('100')) * self.get_total_price()
            elif self.coupon.code.startswith('DE8UG'):
                return self.coupon.discount
        return Decimal('0')

    def get_total_price_after_discount(self):
        if self.coupon.code.startswith('WHOS'):
            return 1
        else:
            return self.get_total_price() - self.get_discount()