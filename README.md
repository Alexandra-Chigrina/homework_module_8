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

mailing_service
├── mailing/ # Приложение сервиса рассылок
│ ├── migrations/ # Миграции базы данных Django
│ ├── templates/ # Шаблоны HTML
│ ├── mailing/ # Шаблоны, относящиеся к приложению mailing
│ ├── urls.py # Маршруты для mailing
│ ├── admin.py # Настройка админки Django
│ ├── views.py # Контроллеры отображения страниц и обработки форм
│ ├── services.py # Бизнес-логика
│ ├── models.py # Модели: Client, Message, Mailing, MailingAttempt
│ ├── forms.py # Кастомные формы
│ ├── management/commands/ # Кастомные команды
│ ├── templatetags # Пользовательские шаблонные теги
│
├── users/ # Приложение для управления пользователями
│ ├── templates/users/ # Шаблоны регистрации, логина, профиля
│ ├── forms.py # Формы для регистрации и профиля
│ ├── models.py # Кастомная модель пользователя
│ ├── views.py # Представления для регистрации, логина, профиля
│ ├── urls.py # Маршруты users
│
├── config/ # Конфигурация проекта Django
│ ├── settings.py # Основные настройки проекта
│ ├── urls.py # Маршруты для всего проекта
│
├── media/ # Медиафайлы, загруженные пользователями
│ ├── mailing/images.py
│ ├── user/avatars .py
│
├── static/ # Статические файлы (CSS, JS, изображения)
│ ├── css/                         
│ ├── bootstrap.min.css # Bootstrap стилизация для шаблонов
│ ├── js/                           
│ ├── bootstrap.bundle.min.js # Bootstrap функциональность #
│
├── logs/ # Файл логов
│
├── manage.py # Управляющий файл Django-проекта
├── .venv # Виртуальное окружение
├── .gitignore # Исключения файлов из Git
├── .flake8 # Настройки линтера Flake8
├── .poetry.lock # Фиксированные зависимости проекта  
├── .pyproject.toml # Основной конфигурационный файл проекта  
├── .env # Переменные окружения (не загружается в Git)
├── .env .sample # Шаблон .env
├── README.md # Документация  
