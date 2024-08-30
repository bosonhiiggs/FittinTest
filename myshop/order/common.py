from django.conf import settings
from django.core.mail import send_mail

from dadata import Dadata


def send_order_email(email, total_sum):
    subject = f'Ваш заказ Fur&Coat'
    message = (f'Здравствуйте!\n'
               f'Ваш заказ на сумму: {total_sum} уже собирается'
               )
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
    )
