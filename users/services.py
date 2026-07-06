import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_payment(amount, course_name, success_url, cancel_url):
    """Создаёт ссылку на оплату одной функцией"""
    try:
        # Создаём продукт
        product = stripe.Product.create(name=course_name)

        # Создаём цену (сумма в копейках)
        price = stripe.Price.create(
            unit_amount=int(amount * 100),
            currency='usd',
            product=product.id
        )

        # Создаём сессию оплаты
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{'price': price.id, 'quantity': 1}],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
        )

        return {'url': session.url, 'session_id': session.id}
    except Exception as e:
        return {'error': str(e)}
