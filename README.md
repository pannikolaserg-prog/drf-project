# 🧠 Трекер полезных привычек

Backend-часть SPA для трекинга привычек.
Реализовано на **Django REST Framework** с **Celery**, **Redis**, **PostgreSQL** и **Stripe**.

Перед тем, как начать работать с проектом, запустите
программу Docker Desktop на вашем компьютере.
---

## 🚀 Запуск через Docker (рекомендуемый способ)

```bash
# 1. Клонировать репозиторий
git clone https://github.com/pannikolaserg-prog/drf-project/compare/develop...feature-clean-merge

# 2. Создать .env из примера
cp .env.example .env
# Заполнить .env своими данными (ключи, пароли)

# 3. Запустить все сервисы
docker-compose up --build

