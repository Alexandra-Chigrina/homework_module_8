# **Онлайн-платформа для обучения (LMS)**

Проект представляет собой backend-систему онлайн-обучения с курсами, уроками, оплатами, подписками и административной
частью. Все сервисы обёрнуты в Docker-контейнеры.


## **Запуск и настройка проекта через Docker Compose**:

1. Клонируйте репозиторий

```
git@github.com:Alexandra-Chigrina/homework_module_8.git
```

2. В терминале инициализируйте Poetry и активируйте виртуальное окружение

```
poetry init
poetry shell
```

Или, если используете venv:

```commandline
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Создайте .env на основе .env.example

4. Соберите и запустите контейнеры

```commandline
docker-compose up -d --build
```

5. Готово! Проект доступен по адресу:

`http://localhost:8000`

Панель администратора:
`http://127.0.0.1:8000/admin/`

6. Выполнение миграций (если нужно вручную)

```docker-compose exec web python manage.py migrate```

7. Остановка проекта

```docker-compose down```


## **Проверка работоспособности сервисов**:

1. Django (web)

Проверить административную панель: 
```http://localhost:8000/admin/```
Если работает — веб-сервер запущен.

2. PostgreSQL (db)

Можно подключиться через PgAdmin или выполнить команду:
```docker exec -it homework_module_8-db-1 psql -U postgres -d module8 -c "SELECT 1;"```
Если видите (1 row) — всё в порядке.

3. Celery

Посмотреть логи воркера:
```docker-compose logs -f celery```

4. Celery Beat

Планировщик автоматически запускает задачи по расписанию.

Проверка:
```docker-compose logs -f celery-beat```
Если вы видите Scheduler: Sending due task deactivate_inactive_user — работает.


## Возможности проекта

### Пользователи и аутентификация
- Регистрация и логин по email
- JWT-авторизация
- Профиль пользователя
- Группы и права доступа

### Курсы и уроки
- CRUD для курсов и уроков
- Только владелец или модератор может изменять
- Подсчёт количества уроков в курсе
- Валидация ссылок

### Платежи и подписки
- Привязка оплат к контенту
- История транзакций
- Проверка доступа по подписке

### Celery + Beat
- Плановая деактивация неактивных пользователей
- Работа фоновых задач

### Swagger
- Описание всех API
- Удобный интерфейс по адресу /swagger/

### Тестирование
```docker-compose exec web pytest```


## Стек технологий

- Django + DRF
- PostgreSQL
- Celery + Redis
- JWT (SimpleJWT)
- Docker, docker-compose
- Swagger (drf-yasg)

## **Структура проекта**

homework_module_8
├── config/                         # Конфигурация проекта Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py                   # Настройки Celery
│   ├── settings.py                 # Основные настройки проекта
│   ├── urls.py                     # Главные маршруты проекта
│   └── wsgi.py
│
├── lms/                            # Приложение с курсами, уроками, подписками
│   ├── management/                 # Кастомные Django-команды
│   ├── migrations/                 # Миграции базы данных для приложения lms
│   │   └── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                   # Кастомные модели (Course, Lesson, Subscription)
│   ├── paginators.py               # Кастомные пагинаторы
│   ├── serializers.py              # Сериализаторы
│   ├── tasks.py                    # Celery-задачи, связанные с LMS
│   ├── views.py                    # View-контроллеры
│   ├── validators.py               # Валидаторы моделей/сериализаторов
│   ├── urls.py                     # Маршруты lms
│   └── tests/                      # Тесты
│
├── users/                          # Приложение управления пользователями
│   ├── management/                 # Кастомные Django-команды
│   ├── migrations/                 # Миграции базы данных для users
│   │   └── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                   # Кастомная модель User
│   ├── permission.py               # DRF-разрешения
│   ├── serializers.py              # Сериализаторы пользователя
│   ├── tests.py                    # Тесты
│   ├── tasks.py                    # Фоновые задачи Celery (например, деактивация)
│   ├── urls.py                     # Маршруты users
│   └── views.py                    # View-контроллеры (регистрация, профиль)
│
├── media/                          # Директория для хранения медиафайлов (если используются)
│
├── .coverage                       # Файл покрытия тестами
├── htmlcov/                        # Отчёты покрытия тестов
├── manage.py                       # Управляющий файл Django
├── .venv                           # Виртуальное окружение
├── .env                            # Файл с переменными окружения
├── .env.sample                     # Пример .env файла
├── .gitignore                      # Исключения Git
├── Dockerfile                      # Сборка образа Django-приложения
├── docker-compose.yml              # Docker-оркестрация всех сервисов
├── .flake8                         # Настройки линтера flake8
├── poetry.lock                     # Фиксация зависимостей Poetry
├── pyproject.toml                  # Основной конфиг проекта
├── README.md                       # Документация проекта
