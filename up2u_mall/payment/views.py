from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from orders.models import Order
from .alipay_de8ug import call_alipay

# Create your views here.
def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    print(order)
    if order:
        subject = f'我的订单{order_id}'
        # total_amount = order.get_total_cost()  # 数据格式错误
        total_amount = float(order.get_total_cost()) # 处理错误码：INVALID_PARAMETER
        print(subject, f'总金额：{total_amount}')
        pay_url = call_alipay(order_id, total_amount, subject)
        # 重定向到支付宝支付页面
        return HttpResponseRedirect(pay_url)


def payment_done(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    print(order)

    # 优惠券失效
    if order.coupon:
        order.coupon.active = False
        order.coupon.save() 

    # 取支付宝返回的参数
    params = request.GET.dict()
    print(params)
    
    # http://localhost:8000/payment/done/?charset=utf-8&out_trade_no=4&method=alipay.trade.page.pay.return&total_amount=200.00&sign=j%2F%2BFvVS3%2FGZalZp5U%2FnOpa%2BzUgKtAY9cEADC8yENz3eMvb74mTsoxKiWysE9rVggpEvUcmGycqa1AidM1CPr16DIeb8mzwjvrcjWnUerP6KNxkfJvslho5y5XUl7hfK9b%2FNClvkgZkkVOa2f7c%2FxVDUP5mlOQgLj13kFrsnuxLaC2P%2BVtZtFcRKLIURYSb%2FkEuVTSUR%2FkX6ERJ68HBUfG1cEOnV1uU0j3JcHyw7IZ4%2BjVSy8MHRU2FTq%2B3W99%2BJO0zEfIDrcUb79WqTBPQdAY38oi8tdfbNBepr6Xhi5G6BWNq6t3PtMhmZg3%2B0%2BhNrm3xZZ51GLKPkE8LEAhSj0%2BA%3D%3D&trade_no=2019012422001416030500344044&auth_app_id=2016092400587584&version=1.0&app_id=2016092400587584&sign_type=RSA2&seller_id=2088102177100122&timestamp=2019-01-24+13%3A35%3A07
    trade_no = params.pop('trade_no', None)  # 取出trade_no
    # 确认支付
    order.paid = True
    # 保存支付宝订单号
    order.pay_id = trade_no
    order.save()

    return render(request, 'payment/done.html', {'trade_no':trade_no})
