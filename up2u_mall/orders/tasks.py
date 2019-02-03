from celery import task
from django.core.mail import send_mail
from .models import Order

@task
def order_created(order_id):
    """
    订单创建成功后，发送邮件通知
    """
    order = Order.objects.get(id=order_id)
    subject = '订单号 {}'.format(order.id)
    message = '你好， {},\n\n下单成功，\
                  订单号为 {}.'.format(order.name,
                                            order.id)

    print(order, subject)
    print('异步发送订单邮件通知...')
    
    html_message = f"""
                    <h1>hi {order.name}</h1>
                    订单{order.id}创建成功。
                    请点击链接返回订单列表
                    <br/>
                    <a href="http://127.0.0.1:8000/orders/" target="_blank">http://127.0.0.1:8000/orders/</a>
                """
                
    mail_sent = send_mail(subject,
                          message,
                          'sublime11@qq.com',
                          [order.email],
                          html_message=html_message)
    return mail_sent
