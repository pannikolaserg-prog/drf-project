import stripe

from django.conf import settings
from django.core.mail import send_mail

from users.models import Status_Pay

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_payment(user, amount, course_id=None):
    """
    Создание платежа в Stripe

    Args:
        user: объект пользователя
        amount: сумма в копейках
        course_id: ID курса (опционально)

    Returns:
        dict: {payment_url, session_id} или {error}
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        # Создаём сессию оплаты
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': f'Оплата от {user.email}',
                    },
                    'unit_amount': int(amount),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:8000/api/payments/success/',
            cancel_url='http://localhost:8000/api/payments/cancel/',
            metadata={
                'user_id': user.id,
                'amount': str(amount),
                'course_id': str(course_id) if course_id else '',
            }
        )

        # Сохраняем платёж в БД
        status_pay = Status_Pay.objects.create(
            user=user,
            amount=amount,
            session_id=session.id,
            link=session.url
        )

        return {
            'success': True,
            'payment_url': session.url,
            'session_id': session.id,
            'payment_id': status_pay.id,
        }

    except stripe.error.StripeError as e:
        return {
            'success': False,
            'error': str(e),
        }

def send_email(subject, message, recipient_email):
    """Отправка письма"""
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=False,
        )
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}
