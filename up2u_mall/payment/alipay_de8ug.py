import webbrowser
from django.conf import settings
from alipay import AliPay
# https://github.com/fzlee/alipay/blob/master/README.zh-hans.md#alipay.trade.page.pay
# pip install python-alipay-sdk --upgrade

app_private_key_string = open(settings.APP_PRIVATE_KEY_PATH).read()
alipay_public_key_string = open(settings.ALIPAY_PUBLIC_KEY_PATH).read()


def call_alipay(order_no, total_amount, subject="测试订单", return_url=settings.ALIPAY_APP_RETURN_URL):
    alipay = AliPay(
        appid=settings.ALIPAY_APP_ID,  # 自己创建的或者沙箱给的id
        app_notify_url=settings.ALIPAY_APP_NOTIFY_URL,  # 默认回调url
        app_private_key_string=app_private_key_string,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2", # RSA 或者 RSA2
        debug=settings.ALIPAY_DEBUG  # 默认False
    )

    # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
    # 测试时候使用沙箱地址
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_no,
        total_amount=total_amount,
        subject=subject,
        return_url=return_url,
    )

    print(order_string)

    pay_url = settings.ALIPAY_GATEWAY_URL + order_string
    return pay_url


if __name__ == "__main__":
    pay_url = call_alipay(111, 11)
    webbrowser.open(pay_url)
