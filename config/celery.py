from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Установка переменной окружения для настроек проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создание экземпляра объекта Celery
app = Celery('config')

# Загрузка настроек из файла Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение и регистрация задач из файлов tasks.py
app.autodiscover_tasks()

# Настройка периодических задач (Celery Beat)
app.conf.beat_schedule = {
    # Задание 3: Блокировка неактивных пользователей (ежедневно в 3:00)
    'block-inactive-users': {
        'task': 'users.tasks.block_inactive_users',
        'schedule': crontab(hour=3, minute=0),
    },
}
