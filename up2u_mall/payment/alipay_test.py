import webbrowser
from alipay import AliPay
# https://github.com/fzlee/alipay/blob/master/README.zh-hans.md#alipay.trade.page.pay
# pip install python-alipay-sdk --upgrade

app_private_key_string = open("alipay_keys/app_private.key").read()
alipay_public_key_string = open("alipay_keys/alipay_public.key").read()


alipay = AliPay(
    appid="2016092400587584",  # 自己创建的或者沙箱给的id
    app_notify_url=None,  # 默认回调url
    app_private_key_string=app_private_key_string,
    # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
    alipay_public_key_string=alipay_public_key_string,
    sign_type="RSA2", # RSA 或者 RSA2
    debug=False  # 默认False
)

subject = "测试订单"

# 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
order_no = input('输入订单号：')
order_string = alipay.api_alipay_trade_page_pay(
    out_trade_no=order_no,
    total_amount=0.81,
    subject=subject,
    return_url="http://localhost:8000/payment/process/",
    notify_url="http://118.24.94.243:5000/" # 可选, 不填则使用默认notify url
)

print(order_string)


# 测试沙箱链接
# https://openapi.alipaydev.com/gateway.do? + order_string
# https://openapi.alipaydev.com/gateway.do?

pay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string
webbrowser.open(pay_url)

# 同步返回的url
# https://example.com/?charset=utf-8&out_trade_no=12314&method=alipay.trade.page.pay.return&total_amount=0.81&sign=BxA7SLGeKF%2B%2Fg6GUYbFCY9NGW3nRZl7g7EUaqrHWdt1OyIK7%2BC7MVMDvzm21KkaCTujwuUrDEIUeQfuDlvwdRiWu%2BM2xVC6BMQgq2ZFGKQpDhqqv1Wr8HBukeYzrQgheVjkQbFPCb4yZCfk%2Fk8%2B8I%2F%2BWdFWBtHpK2Zq7HS5y5V2Wg18N6GhK6yoJAikJwFM7LquMmmXRd9dWc9xeOGx3%2BJJdFb2fE3pT%2FcTF3j97Dne%2BD0OQQGIooUXxf1SIKU2pOJZLI%2FhH72cohnqH0TtbBpzA0mrJTZrUsE4%2B8BRzNjw62KYKmxFrW8N9OsXkqc7kJDVagbJyyn0V7vyJpma%2FrQ%3D%3D&trade_no=2019011122001416030500335633&auth_app_id=2016092400587584&version=1.0&app_id=2016092400587584&sign_type=RSA2&seller_id=2088102177100122&timestamp=2019-01-11+10%3A35%3A47