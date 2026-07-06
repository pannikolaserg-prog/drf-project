from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import User, Subscription
from materials.models import Course, Lesson


@shared_task
def send_course_update_email(course_id, user_email, course_name):
    """Задание 2: Отправка письма об обновлении курса"""
    subject = f'Обновление курса "{course_name}"'
    message = f'''
    Здравствуйте!

    Курс "{course_name}" был обновлён.
    Новые материалы доступны для изучения.

    С уважением,
    Команда проекта
    '''

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        fail_silently=False,
    )
    return f'Email sent to {user_email}'


@shared_task
def notify_subscribers_about_course_update(course_id):
    """Задание 2: Уведомление всех подписчиков курса об обновлении"""
    from .models import Subscription
    from materials.models import Course

    try:
        course = Course.objects.get(id=course_id)
        subscribers = Subscription.objects.filter(course=course).select_related('user')

        emails = [sub.user.email for sub in subscribers if sub.user.email]

        for email in emails:
            send_course_update_email.delay(course_id, email, course.name)

        return f'Notified {len(emails)} subscribers about course "{course.name}"'
    except Course.DoesNotExist:
        return f'Course {course_id} not found'


@shared_task
def block_inactive_users():
    """Задание 3: Блокировка пользователей, не заходивших более месяца"""
    one_month_ago = timezone.now() - timedelta(days=30)

    inactive_users = User.objects.filter(
        last_login__lt=one_month_ago,
        is_active=True,
        is_superuser=False,  # Не блокируем суперпользователей
        is_staff=False,  # Не блокируем сотрудников
    )

    count = inactive_users.count()

    for user in inactive_users:
        user.is_active = False
        user.save()
        # Опционально: отправить письмо о блокировке
        send_account_blocked_email.delay(user.email)

    return f'Blocked {count} inactive users'


@shared_task
def send_account_blocked_email(user_email):
    """Отправка письма о блокировке аккаунта"""
    subject = 'Ваш аккаунт заблокирован'
    message = '''
    Здравствуйте!

    Ваш аккаунт был заблокирован из-за длительного отсутствия активности.
    Для разблокировки обратитесь к администратору.

    С уважением,
    Команда проекта
    '''

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        fail_silently=False,
    )
