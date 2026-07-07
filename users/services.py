import stripe
from django.conf import settings
from users.models import Status_Pay

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_payment(user, amount, course_name="Оплата"):
    """Создание платежа в Stripe (продукт → цена → сессия)"""
    try:
        # Шаг 1: Создаём продукт
        product = stripe.Product.create(
            name=course_name,
            description=f"Оплата от {user.email}"
        )

        # Шаг 2: Создаём цену (сумма в копейках!)
        price = stripe.Price.create(
            unit_amount=int(amount * 100),
            currency='usd',
            product=product.id
        )

        # Шаг 3: Создаём сессию оплаты
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{'price': price.id, 'quantity': 1}],
            mode='payment',
            success_url='http://localhost:8000/api/payments/success/',
            cancel_url='http://localhost:8000/api/payments/cancel/',
        )

        # Сохраняем в БД
        payment = Status_Pay.objects.create(
            user=user,
            amount=int(amount * 100),
            session_id=session.id,
            link=session.url
        )

        return {'success': True, 'payment_url': session.url, 'payment_id': payment.id}

    except Exception as e:
        return {'success': False, 'error': str(e)}
