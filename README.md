# DRF Project

## Локальный запуск

```bash
# 1. Клонировать проект
git clone https://github.com/username/drf-project
cd drf-project

# 2. Создать .env из примера
cp .env.example .env

# 3. Запустить все сервисы
docker-compose up -d

# 4. Применить миграции
docker-compose exec web python manage.py migrate

# 5. Создать суперпользователя
docker-compose exec web python manage.py createsuperuser