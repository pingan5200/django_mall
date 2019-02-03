from django.shortcuts import render, redirect
from django.urls import reverse

from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from coupons.forms import CouponApplyForm

# Create your views here.
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # order = form.save()
            # 考虑优惠
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()

            print(order)
            for item in cart:
                OrderItem.objects.create(order=order,
                                        product=item['product'],
                                        price=item['price'],
                                        quantity=item['quantity'])
            cart.clear()
            # 异步发通知
            order_created(order.id)

            # 去支付
            request.session['order_id'] = order.id
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()

    
    # 优惠券
    coupon_form = CouponApplyForm()

    return render(request,
            'orders/order/create.html',
            {'cart': cart, 
            'form': form,
            'coupon_form': coupon_form })


def orders(request):
    orders = OrderItem.objects.all()
    return render(request,
                  'orders/order/list.html',
                  {'orders': orders}) 